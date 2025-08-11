import { cookies } from "next/headers";
// import { authUser } from "@/api";

export default async function Profile() {
  const cookieStore = await cookies();
  const access_token = cookieStore.get("access_token");
  // get current user
  // useEffect(() => {
  //   const fetchUserSession = async () => {
  //     const { data } = await authUser();
  //     console.log(data);
  //     setCurrentUser("Nombre de usuario");
  //   };

  //   fetchUserSession();
  // }, []);

  console.log(access_token);

  return (
    <main>
      <div className="px-9 pt-5">Google Auth</div>
      <div className="px-9 py-5">Nombre:</div>
    </main>
  );
}
