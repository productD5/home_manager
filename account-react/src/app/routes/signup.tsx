import React , { useState } from 'react';
import axios from 'axios'
import { useNavigate } from 'react-router-dom'
import Header from '../../components/ui/header';
import { GoArrowLeft } from "react-icons/go";
import { paths } from '../../config/paths';
import { Link } from 'react-router-dom';

import '../../components/style/singup.css';

const Signup = () =>{
        const [user_id, setUser_Id] = useState('')
        const [password, setPassword] = useState('')
        const [password_confirmation, setPassword_Confirm] = useState('')
        const [nickname, setNickname] = useState('') 

        const navigate = useNavigate();

        const [error, setError] = useState<string | null>(null);

        const handleSubmit = async (e:React.FormEvent) => {
            e.preventDefault(); //フォームの送信をキャンセル

            if (password !== password_confirmation) {
                // パスワードと確認用パスワードが一致しない場合の処理
                alert('パスワードが一致しません');
                return;
            }
            try {
                const response = await axios.post('http://localhost:8000/accounts/signup/', {
                    user_id: user_id,
                    nickname: nickname,
                    password: password,
                    password_confirmation: password_confirmation
                });
                alert('アカウントが作成されました');
                navigate('/login');
            } catch (error){
                setError('アカウントの作成に失敗しました');
            }
        };
            return (
                <>
                <Header/>
                <div className='main'>
                    <div className='backbox'>

                        <h1>アカウント新規登録</h1>
                        <Link to={paths.Welcome.getHref() } className='back-link' >
                            <GoArrowLeft size={30} title='戻る' />
                        </Link>
                            

                        <form onSubmit={handleSubmit} className='signupform'>
                            <div className='inputtext'>
                                <label htmlFor="user_id">ユーザーID:</label>
                                <input type="text" id="user_id" value={user_id} onChange={(e) => setUser_Id(e.target.value)} />
                            
                            
                                <label htmlFor="nickname">ニックネーム:</label>
                                <input type="text" id="nickname" value={nickname} onChange={(e) => setNickname(e.target.value)} />
                            
                            
                                <label htmlFor="password">パスワード:</label>
                                <input type="password" id="password" value={password} onChange={(e) => setPassword(e.target.value)} />
                            
                            
                                <label htmlFor="password_confirm">パスワード確認:</label>
                                <input type="password" id="password_confirm" value={password_confirmation} onChange={(e) => setPassword_Confirm(e.target.value)} />
                            </div>

                            <button type="submit" className='submitButton'>登録</button>
                        </form>
                    </div>
                </div>
                </>
            );
        };

export default Signup