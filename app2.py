from supabase import create_client, Client



url: str = "https://ljismkbnmwvuisvibyka.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxqaXNta2JubXd2dWlzdmlieWthIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzkwMzk5MDUsImV4cCI6MjA1NDYxNTkwNX0.S48FLYIvSSba25TBcWlWfoLFbMIZywHaRDi0pI3SBRM"


supabase: Client = create_client(url, key)

def get_users():
    response = supabase.table('users').select('*').execute()
    return response.data

if __name__ == "__main__":
    users = get_users()
    print(users)
