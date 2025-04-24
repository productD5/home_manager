import { useState,useEffect } from 'react';
import axios from 'axios';
const Home = () => {
    const [user, setUser] = useState();

    useEffect( () => {
        axios.get('http://localhost:8000/accounts/user/')
            .then((response) => {
                if (response.status === 200) {
                    setUser(response.data);
                } else {
                    console.error('Failed to fetch user data');
                }
            })
            .catch((error) => {
                console.error('Error fetching user data:', error);
        });
        }
    )
    return (
        <>
            <h1>Home</h1>
        </>
    );
};
export default Home;