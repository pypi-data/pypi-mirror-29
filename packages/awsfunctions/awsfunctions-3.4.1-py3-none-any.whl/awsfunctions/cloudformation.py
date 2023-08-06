import json
import logging
import uuid
from datetime import datetime
from typing import Optional

import boto3
from botocore.exceptions import ClientError, WaiterError


def find_export(name: str, cfn_client: object = None) -> Optional[str]:
    """
    Finds values exported as Outputs across all Cloudformation stacks

    Creates a new "boto3.client('cloudformation')" client unless 'cfn_client' is provided. This is not
    recommended except for testing purposes.

    :return: the exported value, or None if the value is not found
    """
    return _find_export_recursively(None, name, cfn_client=cfn_client)


def _find_export_recursively(next_token: Optional[str],
                             name: str,
                             cfn_client: object = None) -> Optional[str]:
    client = cfn_client if cfn_client else boto3.client('cloudformation')
    response = client.list_exports(
        NextToken=next_token) if next_token else client.list_exports()
    exports = response['Exports']
    search = list(filter(lambda x: x['Name'] == name, exports))
    if len(search) > 0:
        return search[0]['Value']
    elif 'NextToken' in response.keys():
        return _find_export_recursively(response['NextToken'], name,
                                        cfn_client)
    else:
        return None


def deploy(stack_name: str,
           template_body: str = "",
           template_file: str = "",
           template_s3_url: str = "",
           parameters: list = [],
           capabilities: list = []) -> dict:
    """
    Creates or updates a cloudformation stack.
        * Either a template body (a string), a s3 url or a local file must be provided.
        * If a stack creation fails, the stack is subsequently deleted

    :return: the stack description after a succesful deployment

    See:
        http://boto3.readthedocs.io/en/latest/reference/services/cloudformation.html#CloudFormation.Client.create_stack
        http://boto3.readthedocs.io/en/latest/reference/services/cloudformation.html#CloudFormation.Client.update_stack
    """

    if not template_body and not template_s3_url and not template_file:
        raise ValueError(
            "either 'template_body', 'template_file' or 'template_s3_url' must be defined"
        )

    params = {
        'StackName': stack_name,
        'Parameters': parameters,
        'Capabilities': capabilities,
    }

    if template_body:
        params['TemplateBody'] = template_body
    elif template_file:
        params['TemplateBody'] = _read_file(template_file)
    else:
        params['TemplateURL'] = template_s3_url

    client = boto3.client('cloudformation')

    try:
        if _stack_exists(stack_name):
            logging.info('updating stack: ' + stack_name)
            client.update_stack(**params)
            waiter = client.get_waiter('stack_update_complete')
        else:
            logging.info('creating stack: ' + stack_name)
            params['OnFailure'] = 'DELETE'
            client.create_stack(**params)
            waiter = client.get_waiter('stack_create_complete')
        logging.info("...waiting for stack to be ready...")
        waiter.wait(StackName=stack_name)
    except ClientError as ex:
        error_message = ex.response['Error']['Message']
        if error_message == 'No updates are to be performed.':
            logging.info(error_message)
        else:
            raise
    result = client.describe_stacks(StackName=stack_name)
    logging.info(json.dumps(result, default=_json_serializer))
    return result["Stacks"][0]


def deploy_with_change_set(stack_name: str,
                           template_body: str = "",
                           template_file: str = "",
                           template_s3_url: str = "",
                           parameters: list = [],
                           capabilities: list = []) -> dict:
    """
    Same as deploy(), but using create_change_set and update_change_set to allow templates containing transforms
    such as "Transform: AWS::Serverless-2016-10-31"

    WARNING: this method is not tested properly due to lack of moto library support for mocks. Please use deploy()
    unless the use of transforms is a requirement.
    """

    if not template_body and not template_s3_url and not template_file:
        raise ValueError(
            "either 'template_body', 'template_file' or 'template_s3_url' must be defined"
        )

    stack_exists = _stack_exists(stack_name)

    change_set_name = stack_name + "-change-set-" + str(uuid.uuid4())[:8]

    params = {
        'StackName': stack_name,
        'Parameters': parameters,
        'Capabilities': capabilities,
        'ChangeSetName': change_set_name,
        'ChangeSetType': 'UPDATE' if stack_exists else 'CREATE'
    }

    if template_body:
        params['TemplateBody'] = template_body
    elif template_file:
        params['TemplateBody'] = _read_file(template_file)
    else:
        params['TemplateURL'] = template_s3_url

    client = boto3.client('cloudformation')

    try:
        client.create_change_set(**params)
        client.get_waiter('change_set_create_complete').wait(
            StackName=stack_name, ChangeSetName=change_set_name)
        client.execute_change_set(
            StackName=stack_name, ChangeSetName=change_set_name)
        waiter_name = 'stack_update_complete' if stack_exists else 'stack_create_complete'
        client.get_waiter(waiter_name).wait(StackName=stack_name)
    except WaiterError as ex:
        if "submitted information didn't contain changes" in ex.last_response[
                'StatusReason']:
            logging.info(ex.last_response['StatusReason'])
        else:
            raise
    result = client.describe_stacks(StackName=stack_name)
    logging.info(json.dumps(result, default=_json_serializer))
    return result["Stacks"][0]


def _stack_exists(stack_name: str) -> bool:
    client = boto3.client('cloudformation')
    stacks = client.list_stacks()['StackSummaries']
    for stack in stacks:
        if stack['StackStatus'] == 'DELETE_COMPLETE':
            continue
        if stack_name == stack['StackName']:
            return True
    return False


def _read_file(template_file: str) -> str:
    with open(template_file) as template_fileobj:
        template_data = template_fileobj.read()
    return template_data


def _json_serializer(obj: object) -> str:
    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError("Type not serializable")
