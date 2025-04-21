import React from "react";
import Header from "../../components/ui/header";
import "../../components/style/welcome.css"
import { Link } from "react-router-dom";
import {paths} from "../../config/paths"

const Welcome = () =>{
    return(
    <div className="back-box">
        <Header/>
        <Link to={paths.Login.getHref()}>
        <button>ログイン</button>
        </Link>
        <Link to={paths.sign_up.getHref()}>
        <button>新規登録</button>
        </Link>
    </div>
    );
};

export default Welcome