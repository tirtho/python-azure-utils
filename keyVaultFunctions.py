# Setup
# pip install azure.identity
# pip install azure-keyvault-secrets
# Make sure Azure Key Vault exists in your Azure account
# https://docs.microsoft.com/en-us/azure/key-vault/secrets/quick-create-python?tabs=cmd

from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from azure.identity import InteractiveBrowserCredential

# Using the Interactive Browser Credential to authenticate
def akvConnect(keyVaultName):
    akvUri = f"https://{keyVaultName}.vault.azure.net"
    credential = InteractiveBrowserCredential() #DefaultAzureCredential()
    client = SecretClient(vault_url=akvUri, credential=credential)
    return client

def akvGetSecret(akvConnection, secretName):
    return akvConnection.get_secret(secretName)

def akvSetSecret(akvConnection, secretName, secretValue):
    akvConnection.set_secret(secretName, secretValue)

def akvDeleteSecret(akvConnection, secretName):
    pollIt = akvConnection.begin_delete_secret(secretName)
    deleted_secret = pollIt.result()
    return deleted_secret
