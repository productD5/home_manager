import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

interface User {
  user_id: string;
  nickname: string;
  email: string;
  comment: string;
}
const Home = () => {
  const userHomeData = [
    {
      money: 1800,
      category: "食費",
      title: "朝ごはん",
      money_comment: "パンとコーヒー",
    },
    {
      money: 4500,
      category: "日用品",
      title: "ドラッグストア",
      money_comment: "洗剤とトイレットペーパー",
    },
    {
      money: 12000,
      category: "交通費",
      title: "定期券購入",
      money_comment: "通勤用6ヶ月定期",
    },
    {
      money: 3000,
      category: "趣味",
      title: "映画",
      money_comment: "映画鑑賞とポップコーン",
    },
    {
      money: 8000,
      category: "交際費",
      title: "飲み会",
      money_comment: "会社の歓迎会",
    },
  ];
  const [user, setUser] = useState<User | null>(null);
  const navigate = useNavigate();
  const logout = () => {
    navigate("/login");
  };
  useEffect(() => {
    const user_id = localStorage.getItem("user_id");
    const nickname = localStorage.getItem("nickname");

    console.log(user_id);
    if (!user_id) {
      alert("ログインしてください");
      logout();
      return;
    }

    console.log(user_id);
    const apipath = "http://localhost:8000/accounts/users/" + user_id + "/";
    axios
      .get(apipath)
      .then((response) => {
        if (response.status === 200) {
          setUser(response.data.user);
        } else {
          console.error("Failed to fetch user data");
        }
      })
      .catch((error) => {
        console.error("fetchに失敗しました:", error);
      });
  }, []);

  return (
    <>
      <h2>ようこそ、{user?.nickname}さん</h2>
      <h3>最近の支出</h3>

      {userHomeData.map((data, index) => (
        <div key={index} className="home-data">
          <h4>{data.category}</h4>
          <p>金額: {data.money}円</p>
          <p>タイトル: {data.title}</p>
          <p>コメント: {data.money_comment}</p>
        </div>
      ))}
    </>
  );
};
export default Home;
