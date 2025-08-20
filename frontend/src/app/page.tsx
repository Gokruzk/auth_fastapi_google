"use client";

import { useEffect, useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL;
const FRONTEND_URL = process.env.NEXT_PUBLIC_FRONT_URL;
const allowedOrigins = [`${FRONTEND_URL}`, `${API_URL}`];

export default function Home() {
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    function handleMessage(event: MessageEvent) {
      if (!allowedOrigins.includes(event.origin)) return;
      const { token } = event.data;
      if (token) {
        setToken(token);
        localStorage.setItem("access_token", token);
      }
    }

    window.addEventListener("message", handleMessage);

    return () => {
      window.removeEventListener("message", handleMessage);
    };
  }, []);

  function openLoginPopup() {
    const width = 500;
    const height = 600;
    const left = window.innerWidth / 2 - width / 2;
    const top = window.innerHeight / 2 - height / 2;

    window.open(
      `${API_URL}/api/v1/auth/login/google`,
      "Login with Google",
      `width=${width},height=${height},top=${top},left=${left}`
    );
  }

  return (
    <main>
      <div className="px-9 pt-5">Google Auth</div>
      <div className="px-9 py-5">
        {!token ? (
          <button
            onClick={openLoginPopup}
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 mr-2 rounded"
          >
            Login
          </button>
        ) : (
          <div>¡Autenticado!</div>
        )}
      </div>
    </main>
  );
}
