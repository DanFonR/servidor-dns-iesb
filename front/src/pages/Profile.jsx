import { useLocation } from "react-router-dom";

export default function Profile() {
  const location = useLocation();

  return (
    <div className="profile-container">
      <h2>Profile</h2>
      <h4>username: </h4>
      <h4>server name: </h4>
    </div>
  );
}
