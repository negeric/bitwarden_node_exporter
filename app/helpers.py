import sqlite3, os, logging
from pathlib import Path

parent = Path(__file__).parent
logging.basicConfig(level=os.environ.get("BW_LOGLEVEL", "INFO"))
logging.info(f"Parent {parent}")
db_path = os.getenv('BW_DB_PATH', '/data/db.sqlite3')
attachments_path = os.getenv('BW_ATTACH_PATH', '/data/attachments')

def get_counts():
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        logging.info("Connected to SQLite Database")
    except:
        logging.error("Error connnecting to the SQLite DB.  Verify the BW_DATA_PATH env var")
        return error
    try:
        ## Users
        users_query = "SELECT COUNT(*) FROM users"
        users = cursor.execute(users_query).fetchone()[0]

        ## Users with MFA
        mfa_query = "SELECT COUNT(*) FROM twofactor"
        mfa = cursor.execute(mfa_query).fetchone()[0]

        ## Organizations
        org_query = "SELECT COUNT(*) FROM organizations"
        org = cursor.execute(org_query).fetchone()[0]

        ## Collections
        collections_query = "SELECT COUNT(*) FROM collections"
        collections = cursor.execute(collections_query).fetchone()[0]

        ## Passwords
        pass_query = "SELECT COUNT(*) FROM ciphers"
        passwords = cursor.execute(pass_query).fetchone()[0]

        ## Attachments
        attachments_query = "SELECT COUNT(*) FROM attachments"
        attachments = cursor.execute(attachments_query).fetchone()[0]

        ## DB Size
        db_size = os.path.getsize(db_path)

        ## Attachments
        if os.path.exists(attachments_path):
            tmp_path = Path(attachments_path)
            attachment_size = sum(f.stat().st_size for f in tmp_path.glob('**/*') if f.is_file())
        else:
            attachment_size = 0

        return f"bw_users {users}\nbw_mfa_accounts {mfa}\nbw_organizations {org}\nbw_collections {collections}\nbw_passwords {passwords}\nbw_attachments {attachments}\nbw_db_size {db_size}\nbw_attachment_total_size {attachment_size}"
    except:
        logging.exception("Error querying DB")
        return ""
