"""Code Grading Workflow Example.

Demonstrates how to use the multi-agent code grading workflow to evaluate
code quality across multiple dimensions using specialized agents.

This workflow uses:
- Static Analyst: Linting, complexity, duplication
- Test Analyst: Coverage and test quality
- Documentation Reviewer: Docstrings and comments
- Security Auditor: OWASP vulnerabilities
- Dependency Auditor: CVEs and licenses
- Performance Reviewer: Algorithms and resources
- Architecture Compliance: Patterns and separation
- Maintainability Agent: Readability and extensibility
- Best Practices Agent: Framework conventions
- Head Judge: Final grade compilation
"""

import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from multiagent_workflows.core.logger import VerboseLogger
from multiagent_workflows.core.model_manager import ModelManager
from multiagent_workflows.core.workflow_engine import WorkflowEngine

# Sample Python code to grade - intentionally has some issues to demonstrate scoring
SAMPLE_CODE_GOOD = '''
"""
User Authentication Module

Provides secure user authentication with JWT tokens
and proper password hashing.
"""

import hashlib
import hmac
import secrets
from datetime import datetime, timedelta
from typing import Optional
import jwt  # PyJWT library

# Configuration
SECRET_KEY = "your-secret-key-here"  # Note: Should be env variable
ALGORITHM = "HS256"
TOKEN_EXPIRE_HOURS = 24


class InvalidCredentialsError(Exception):
    """Raised when login credentials are invalid."""
    pass


class TokenExpiredError(Exception):
    """Raised when authentication token has expired."""
    pass


def hash_password(password: str, salt: Optional[bytes] = None) -> tuple[str, str]:
    """
    Hash a password using PBKDF2-HMAC-SHA256.
    
    Args:
        password: Plain text password to hash
        salt: Optional salt bytes (generated if not provided)
        
    Returns:
        Tuple of (hashed_password, salt) as hex strings
        
    Example:
        >>> hashed, salt = hash_password("mypassword123")
        >>> verify_password("mypassword123", hashed, salt)
        True
    """
    if salt is None:
        salt = secrets.token_bytes(32)
    
    hashed = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        100000  # iterations
    )
    
    return hashed.hex(), salt.hex()


def verify_password(password: str, hashed: str, salt: str) -> bool:
    """
    Verify a password against its hash.
    
    Args:
        password: Plain text password to verify
        hashed: Previously hashed password (hex string)
        salt: Salt used during hashing (hex string)
        
    Returns:
        True if password matches, False otherwise
    """
    salt_bytes = bytes.fromhex(salt)
    new_hash, _ = hash_password(password, salt_bytes)
    
    # Use constant-time comparison to prevent timing attacks
    return hmac.compare_digest(new_hash, hashed)


def create_token(user_id: str, email: str) -> str:
    """
    Create a JWT authentication token.
    
    Args:
        user_id: Unique user identifier
        email: User's email address
        
    Returns:
        JWT token string
    """
    expiration = datetime.utcnow() + timedelta(hours=TOKEN_EXPIRE_HOURS)
    
    payload = {
        "sub": user_id,
        "email": email,
        "exp": expiration,
        "iat": datetime.utcnow(),
    }
    
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> dict:
    """
    Verify and decode a JWT token.
    
    Args:
        token: JWT token string
        
    Returns:
        Decoded token payload
        
    Raises:
        TokenExpiredError: If token has expired
        InvalidCredentialsError: If token is invalid
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise TokenExpiredError("Authentication token has expired")
    except jwt.InvalidTokenError:
        raise InvalidCredentialsError("Invalid authentication token")


# Unit tests
def test_password_hashing():
    """Test password hashing and verification."""
    password = "secure_password_123"
    hashed, salt = hash_password(password)
    
    assert verify_password(password, hashed, salt) is True
    assert verify_password("wrong_password", hashed, salt) is False


def test_token_creation():
    """Test JWT token creation and verification."""
    token = create_token("user123", "test@example.com")
    payload = verify_token(token)
    
    assert payload["sub"] == "user123"
    assert payload["email"] == "test@example.com"


if __name__ == "__main__":
    # Demo
    print("Testing password hashing...")
    hashed, salt = hash_password("demo_password")
    print(f"Hash: {hashed[:32]}...")
    print(f"Verification: {verify_password('demo_password', hashed, salt)}")
    
    print("\\nTesting token creation...")
    token = create_token("demo_user", "demo@example.com")
    print(f"Token: {token[:50]}...")
'''

SAMPLE_CODE_POOR = """
import os

password = "admin123"  # hardcoded password
db_conn = "postgresql://root:root@localhost/db"  # hardcoded credentials

def check_login(u,p):
    # no validation
    sql = "SELECT * FROM users WHERE user='" + u + "' AND pass='" + p + "'"
    # SQL injection vulnerability
    return True

def get_data(x):
    data = []
    for i in range(len(x)):
        for j in range(len(x)):
            for k in range(len(x)):  # O(n^3) complexity
                data.append(x[i])
    return data

def process(a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p):
    # too many parameters
    temp = a+b+c+d+e 
    temp2 = f+g+h+i+j
    temp3 = k+l+m+n+o+p
    return temp*temp2*temp3
"""


async def run_code_grading_demo():
    """Run the code grading workflow."""
    print("=" * 70)
    print("Multi-Agent Code Grading Workflow Demo")
    print("=" * 70)
    print()

    # Initialize components
    print("Initializing model manager...")
    model_manager = ModelManager(allow_remote=True)

    # Check model availability
    print("\nChecking model availability...")
    available = await model_manager.list_models()
    print(f"  Available models: {len(available)}")

    # Create logger
    logger = VerboseLogger(
        workflow_id=f"code-grading-{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        config={"level": "INFO"},
    )

    # Create workflow engine
    print("Creating workflow engine...")
    engine = WorkflowEngine(model_manager=model_manager)

    # List available workflows
    print("\nAvailable workflows:")
    workflows = engine.list_workflows()
    for wf in workflows:
        print(f"  - {wf}")

    # Prepare inputs
    code_to_grade = SAMPLE_CODE_GOOD  # Use the good example

    print(f"\nCode sample: {len(code_to_grade)} characters")
    print("Sample preview:")
    print("-" * 40)
    print(code_to_grade[:500] + "...")
    print("-" * 40)

    # Run workflow
    print("\n🚀 Starting code grading workflow...")
    print()

    try:
        result = await engine.execute_workflow(
            workflow_name="code_grading",
            inputs={
                "code_submission": code_to_grade,
                "language": "python",
                "context": "Authentication module for a web application",
            },
        )

        print("\n" + "=" * 70)
        print("✅ Workflow Complete!")
        print("=" * 70)

        # Display results
        if result.success:
            outputs = result.outputs

            print(f"\n📊 Execution time: {result.duration_ms:.0f}ms")
            print(f"📋 Steps completed: {len(result.step_results)}")

            # Show step results
            print("\n📝 Step Results:")
            for step_id, step_result in result.step_results.items():
                status = "✅" if step_result.success else "❌"
                print(f"  {status} {step_id}")

            # Show grading outputs if available
            if "overall_grade" in outputs:
                print(f"\n🎓 Overall Grade: {outputs.get('overall_grade', 'N/A')}")

            if "category_scores" in outputs:
                print("\n📈 Category Scores:")
                for category, score in outputs.get("category_scores", {}).items():
                    print(f"  {category}: {score}")

            # Export results
            results_dir = Path("evaluation/results/code_grading")
            results_dir.mkdir(parents=True, exist_ok=True)

            result_file = (
                results_dir / f"grading_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )
            with open(result_file, "w") as f:
                json.dump(
                    {
                        "workflow_id": result.workflow_id,
                        "workflow_name": result.workflow_name,
                        "success": result.success,
                        "duration_ms": result.duration_ms,
                        "outputs": outputs,
                    },
                    f,
                    indent=2,
                    default=str,
                )

            print(f"\n💾 Results saved to: {result_file}")

        else:
            print(f"\n❌ Workflow failed: {result.error}")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()


async def simple_model_test():
    """Test model availability before running full workflow."""
    print("Testing model availability...")

    manager = ModelManager()

    # Check key models used by grading workflow
    models = [
        "local:phi4",  # Static analysis
        "gh:openai/gpt-4o-mini",  # Fast tasks
        "gh:openai/o3-mini",  # Security
        "gh:openai/gpt-4o",  # Head judge
    ]

    print("\nModel Status:")
    for model_id in models:
        try:
            available = await manager.check_availability(model_id)
            status = "✅ Available" if available else "⚠️  Not available"
        except Exception as e:
            status = f"❌ Error: {e}"
        print(f"  {model_id}: {status}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Code Grading Workflow Demo")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Only check model availability",
    )
    parser.add_argument(
        "--poor",
        action="store_true",
        help="Grade the poor quality sample instead",
    )
    args = parser.parse_args()

    if args.check:
        asyncio.run(simple_model_test())
    else:
        asyncio.run(run_code_grading_demo())
