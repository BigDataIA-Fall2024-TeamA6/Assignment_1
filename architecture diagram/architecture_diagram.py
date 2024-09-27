# Install the diagrams library using: pip install diagrams
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.storage import S3
from diagrams.aws.database import RDS
from diagrams.onprem.client import User
from diagrams.custom import Custom

# Path to logos
huggingface_logo = "/Users/sahitinallamolu/NEU/BDIA/architecture diagram/hf-logo.png"
streamlit_logo = "/Users/sahitinallamolu/NEU/BDIA/architecture diagram/streamlit-logo.png"
openai_logo = "/Users/sahitinallamolu/NEU/BDIA/architecture diagram/openai-logo.png"
s3_logo = "/Users/sahitinallamolu/NEU/BDIA/architecture diagram/s3-logo.png"
rds_logo = "/Users/sahitinallamolu/NEU/BDIA/architecture diagram/rds-logo.png"
user_logo = "/Users/sahitinallamolu/NEU/BDIA/architecture diagram/user-logo.png"

# Create the diagram
with Diagram("GAIA Model Evaluation Workflow", show=True):
    
    # Hugging Face GAIA Dataset
    huggingface = Custom("Hugging Face GAIA Dataset", huggingface_logo)

    # Create first box (Cluster for S3 and RDS) at the base level
    with Cluster("Data Sources"):
        s3 = Custom("S3 Bucket", s3_logo)
        rds = Custom("Amazon RDS", rds_logo)

    # Overlay second box (Cluster for Streamlit and OpenAI LLM) on top right corner
    with Cluster("Application Layer"):
        app_server = Custom("App Server", streamlit_logo)
        openai_llm = Custom("OpenAI LLM", openai_logo)

    # User interacts directly with Streamlit app
    user = Custom("User", user_logo)

    # Darker colored arrows with visual increase in length due to placement
    # Data flows from Hugging Face
    huggingface >> Edge(color=	"#704a63", style="bold") >> s3  # Darker blue
    huggingface >> Edge(color="#3b71b9", style="bold") >> rds  # Darker green

    # Streamlit fetching data from S3 and RDS
    app_server >> Edge(color="	#704a63", style="bold") >> s3
    app_server >> Edge(color="#3b71b9", style="bold") >> rds

    # Two-way connection between Streamlit and OpenAI LLM
    app_server >> Edge(color="#8d939c", style="bold") >> openai_llm  # Darker red
    app_server << Edge(color="#8d939c", style="bold") << openai_llm

    # User interaction with Streamlit app
    user >> Edge(color="#000000", style="bold") >> app_server  # Darker black
