"use client"

import { authUser } from "@/api";
import { useEffect, useState } from "react";

export default function Profile() {
  const [currentUser, setCurrentUser] = useState<string | undefined>();

  // get current user
  useEffect(() => {
    const fetchUserSession = async () => {
      const { data } = await authUser();
      console.log(data);
      setCurrentUser("Nombre de usuario");
    };

    fetchUserSession();
  }, []);

  return (
    <main>
      <div className="px-9 pt-5">Google Auth</div>
      <div className="px-9 py-5">Nombre: {currentUser}</div>
    </main>
  );
}
