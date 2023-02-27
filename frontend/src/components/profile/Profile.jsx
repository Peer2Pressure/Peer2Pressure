import "./profile.css"

export default function Profile() {
  return (
    <div>
        <div className="profileBox">
            <img class="profileImage" src="/assets/johnDoe.jpg" alt="profile of id.name"/>
            <h1 className="nameTitle">
                {/* put id.Name here  */}
                John Doe
            </h1>
            <button className="manageProfileButton">Manage profile</button>
        </div>
    </div>
  )
}
