import { useFetch } from "../hooks/useFetch";

function UserList() {
  const {
    users,
    loading,
    error,
  } = useFetch();

  if (loading) {
    return <h2>Loading...</h2>;
  }

  if (error) {
    return <h2>{error}</h2>;
  }

  return (
    <div>
      <h1>Users</h1>

      {users.map((user) => (
        <div
          key={user.id}
        >
          <h3>{user.name}</h3>
          <p>{user.email}</p>
        </div>
      ))}
    </div>
  );
}

export default UserList;