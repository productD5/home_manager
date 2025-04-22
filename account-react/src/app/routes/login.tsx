import React , { useState } from 'react';
import axios from 'axios'
import { useNavigate } from 'react-router-dom'
import Header from '../../components/ui/header';

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
            localStorage.setItem('user_id', response.data.user_id);
            alert('ログイン成功');
            navigate('/home'); //ログイン成功後にリダイレクト
        }).catch((error) => {
            console.error('Login error:', error);
            setError('ログインに失敗しました。ユーザーIDまたはパスワードが正しいか確認してください。');
        });
    };
    return(
        <>
        <Header/>
        <div className='main'>
            <h1>ログイン</h1>
            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="user_id">ユーザーID:</label>
                    <input type="text" id="user_id" value={user_id} onChange={(e) => setUser_Id(e.target.value)} />
                </div>
                <div>
                    <label htmlFor="password">パスワード:</label>
                    <input type="password" id="password" value={password} onChange={(e) => setPassword(e.target.value)} />
                </div>
                {error && <p style={{ color: 'red' }}>{error}</p>}
                <button type="submit">ログイン</button>
            </form>
        </div>
        </>
    );
};

export default Login