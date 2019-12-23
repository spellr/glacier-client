from collections import namedtuple

Region = namedtuple("Region", ["name", "code"])

REGIONS = [
    Region("US East (Ohio)", "us-east-2"),
    Region("US East (N. Virginia)", "us-east-1"),
    Region("US West (N. California)", "us-west-1"),
    Region("US West (Oregon)", "us-west-2"),
    Region("Asia Pacific (Mumbai)", "ap-south-1"),
    Region("Asia Pacific (Seoul)", "ap-northeast-2"),
    Region("Asia Pacific (Singapore)", "ap-southeast-1"),
    Region("Asia Pacific (Sydney)", "ap-southeast-2"),
    Region("Asia Pacific (Tokyo)", "ap-northeast-1"),
    Region("Canada (Central)", "ca-central-1"),
    Region("EU (Frankfurt)", "eu-central-1"),
    Region("EU (Ireland)", "eu-west-1"),
    Region("EU (London)", "eu-west-2"),
    Region("EU (Paris)", "eu-west-3"),
    Region("EU (Stockholm)", "eu-north-1"),
    Region("South America (Sao Paulo)", "sa-east-1"),
]
