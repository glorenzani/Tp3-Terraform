provider "aws" {
    shared_config_files = ["/Users/germa/.aws/config"]
    shared_credentials_files = ["/Users/germa/.aws/credentials"]
    region  = "us-east-1"
    profile = "default"
}