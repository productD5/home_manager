import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import Header from "@/components/ui/header";
import "@/components/styles/home.css";

import { FaPen } from "react-icons/fa";
import { IoIosAddCircle } from "react-icons/io";

import ModalModel from "@/components/ui/ModalModel";
import EditMoneyForm from "@/features/home/EditMoneyForm";
import AddMoneyForm from "@/features/home/AddMoneyForm";

interface User {
  user_id: string;
  nickname: string;
  email: string;
  comment: string;
}

type MoneyData = {
  money: number;
  category: string;
  title: string;
  money_comment: string;
};
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
  // 選択されたデータを管理
  const [selectedData, setSelectData] = useState<MoneyData>();

  // 編集モーダルの開閉状態を管理
  const [editModalIsOpen, setIsEditModalOpen] = useState(false);

  // 新規追加モーダルの開閉状態を管理
  const [addModalIsOpen, setIsAddModalOpen] = useState(false);
  // ユーザーホームデータの状態を管理
  const [userHomeList, setUserHomelist] = useState(userHomeData);

  const navigate = useNavigate();

  //編集アイコン押下
  const handleEditClick = (moneyData: MoneyData) => {
    console.log("編集アイコンが押されました", moneyData);
    setSelectData(moneyData);
    setIsEditModalOpen(true);
  };

  //編集保存
  const handleSave = (updatedData: MoneyData) => {
    const updatelist = userHomeList.map((item) =>
      item.title === updatedData.title ? updatedData : item
    );
    setUserHomelist(updatelist);
    setIsEditModalOpen(false);
  };

  // 新規追加ボタン押下
  const handleAddMoney = (newData: MoneyData) => {
    setUserHomelist([...userHomeList, newData]);
    setIsAddModalOpen(false);
    alert("新しい出費データを作成しました");
  };

  // ログアウト関数
  const logout = () => {
    navigate("/login");
  };
  // ユーザーデータを取得するためのuseEffect
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
      <Header />
      <h2>ようこそ、{user?.nickname}さん</h2>
      <h3>最近の支出</h3>

      {userHomeList.map((moneyData, index) => (
        <div key={index} className="home-data">
          <div className="home-box">
            <h4>{moneyData.category}</h4>
            <p>金額: {moneyData.money}円</p>
            <p>タイトル: {moneyData.title}</p>
            <p>コメント: {moneyData.money_comment}</p>
            <FaPen
              onClick={() => handleEditClick(moneyData)}
              style={{ fontSize: "20px" }}
            />
          </div>
        </div>
      ))}
      <IoIosAddCircle className="addbutton" onClick={() => handleAddMoney} />

      <ModalModel
        isOpen={editModalIsOpen}
        onClose={() => setIsEditModalOpen(false)}
      >
        {selectedData && (
          <EditMoneyForm moneyData={selectedData} onSave={handleSave} />
        )}
      </ModalModel>

      <ModalModel
        isOpen={addModalIsOpen}
        onClose={() => setIsAddModalOpen(false)}
      >
        {userHomeData && (
          <AddMoneyForm
            moneyData={{
              money: 0,
              category: "",
              title: "",
              money_comment: "",
            }}
            onSave={(newData) => handleAddMoney(newData)}
          />
        )}
      </ModalModel>
    </>
  );
};
export default Home;
