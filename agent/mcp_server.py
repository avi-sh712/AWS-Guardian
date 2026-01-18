from mcp.server.fastmcp import FastMCP
import boto3

mcp = FastMCP("AWS Guardian Server")

@mcp.tool()
def list_ec2_instances() -> str:
    """Lists all EC2 instances, their state, and instance type."""
    ec2 = boto3.client('ec2')
    response = ec2.describe_instances()
    instances = []
    for r in response['Reservations']:
        for i in r['Instances']:
            instances.append({
                "id": i['InstanceId'],
                "state": i['State']['Name'],
                "type": i['InstanceType']
            })
    return str(instances) if instances else "No EC2 instances found."

@mcp.tool()
def check_s3_public_access() -> str:
    """Checks S3 buckets for public access configuration."""
    s3 = boto3.client('s3')
    buckets = s3.list_buckets()['Buckets']
    risk_buckets = []
    for b in buckets:
        try:
            status = s3.get_public_access_block(Bucket=b['Name'])
            config = status['PublicAccessBlockConfiguration']
            if not all(config.values()):
                risk_buckets.append(b['Name'])
        except Exception:
            risk_buckets.append(b['Name'])
    return str(risk_buckets) if risk_buckets else "All buckets are private."

# --- NEW FIX TOOL ---
@mcp.tool()
def enable_s3_public_block(bucket_name: str) -> str:
    """
    SECURITY FIX: Enables 'Block Public Access' for a specific S3 bucket.
    Use this ONLY when authorized by the user to fix a security risk.
    """
    s3 = boto3.client('s3')
    try:
        s3.put_public_access_block(
            Bucket=bucket_name,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': True,
                'IgnorePublicAcls': True,
                'BlockPublicPolicy': True,
                'RestrictPublicBuckets': True
            }
        )
        return f"SUCCESS: Secured bucket '{bucket_name}'."
    except Exception as e:
        return f"FAILED to secure bucket: {str(e)}"

if __name__ == "__main__":
    mcp.run()