import React , { useState } from 'react';
import axios from 'axios'
import { useNavigate } from 'react-router-dom'
import Header from '../../components/ui/header';
import { GoArrowLeft } from "react-icons/go";
import { Link } from 'react-router-dom';
import { paths } from '../../config/paths';
import '../../components/style/from.css';


const Login = () =>{
    const [user_id, setUser_Id] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();
    const [error, setError] = useState<string | null>(null);

    const handleSubmit = async (e:React.FormEvent) => {
        e.preventDefault(); //フォームの送信をキャンセル

        axios.post('http://localhost:8000/accounts/login/', {
            user_id: user_id,
            password: password
        })
        .then((response) => {
            if (response.status === 200) {
            // ログイン成功時の処理
                localStorage.setItem('user_id', response.data.user_id);
                alert('ログイン成功');
                navigate('/home'); //ログイン成功後にリダイレクト
            }
            else {
                alert('ログインに失敗しました。ユーザーIDまたはパスワードが正しいか確認してください。');
            }
        }).catch((error) => {
                setError('ログインに失敗しました。');
        });
    };
    return(
        <>
                <Header/>
                <div className='main'>
                    <div className='backbox'>

                        <h1>ログイン</h1>
                        <Link to={paths.Welcome.getHref() } className='back-link' >
                            <GoArrowLeft size={30} title='戻る' />
                        </Link>
                            

                        <form onSubmit={handleSubmit} className='signupform'>
                            <div className='inputtext'>

                                <label htmlFor="user_id">ユーザーID:</label>
                                <input type="text" id="user_id" value={user_id} onChange={(e) => setUser_Id(e.target.value)} />
                            
                                <label htmlFor="password">パスワード:</label>
                                <input type="password" id="password" value={password} onChange={(e) => setPassword(e.target.value)} />
                            </div>

                            <button type="submit" className='submitButton'>ログイン</button>
                        </form>
                    </div>
                </div>
        </>
    );
};
export default Login