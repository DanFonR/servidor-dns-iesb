import { useLocation } from "react-router-dom";

export default function Login() {
  const location = useLocation();

  return (
    <div className="login-container">
      <h2>Login</h2>
      <form action="/profile" method="post">
        <input type="text" name="username" placeholder="Username" required />
        <input
          type="password"
          name="password"
          placeholder="Password"
          required
        />
        <button type="submit">Sign In</button>
      </form>
    </div>
  );
}
