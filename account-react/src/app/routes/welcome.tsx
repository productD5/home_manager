import React from "react";
import Header from "@/components/ui/header";
import "@/components/styles/welcome.css";
import { Link } from "react-router-dom";
import { paths } from "../../config/paths";

const Welcome = () => {
  return (
    <>
      <Header />
      <div className="main">
        <div className="back-box">
          <Link to={paths.Login.getHref()}>
            <button className="button">ログイン</button>
          </Link>
          <Link to={paths.sign_up.getHref()}>
            <button className="button">新規登録</button>
          </Link>
        </div>
      </div>
    </>
  );
};

export default Welcome;
