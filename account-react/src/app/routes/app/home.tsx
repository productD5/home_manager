import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import Header from "@/components/ui/header";
import "@/components/styles/home.css";

import { FaPen } from "react-icons/fa";
import { IoIosAddCircle } from "react-icons/io";
import { FaTrash } from "react-icons/fa6";

import ModalModel from "@/components/ui/ModalModel";
import EditMoneyForm from "@/features/home/EditMoneyForm";
import AddMoneyForm from "@/features/home/AddMoneyForm";
import { MdOutlineDataArray, MdOutlineExitToApp } from "react-icons/md";
import DeleteModal from "@/features/home/DeleteModal";
import CategoryFilter from "@/features/home/CategoryDatafilter";

type MoneyData = {
  money_id: number;
  money: number;
  category: string;
  title: string;
  money_comment: string;
};

const Home = () => {
  // ユーザーのニックネームを管理
  // 初期値はゲスト
  const [nickname, setNickname] = useState<string>("gest");

  // 選択されたデータを管理
  const [selectedData, setSelectData] = useState<MoneyData>();

  // 編集モーダルの開閉状態を管理
  const [editModalIsOpen, setIsEditModalOpen] = useState(false);

  // 新規追加モーダルの開閉状態を管理
  const [addModalIsOpen, setIsAddModalOpen] = useState(false);

  // 削除モーダルの開閉状態を管理
  const [deleteModalIsOpen, setIsDeleteModalOpen] = useState(false);

  // ユーザーホームデータの状態を管理
  const [userHomeList, setUserHomelist] = useState<MoneyData[]>([]);

  //選択したカテゴリーを管理
  const [selectedCategory, setSelectedCategory] = useState("");

  const navigate = useNavigate();
  //ユニークなcategoryの一覧
  const categorys = Array.from(new Set(userHomeList.map((c) => c.category)));

  //編集アイコン押下
  const handleEditClick = (moneyData: MoneyData) => {
    console.log("編集アイコンが押されました", moneyData);
    setSelectData(moneyData);
    setIsEditModalOpen(true);
  };

  //編集保存
  const handleUpdateSave = (updatedData: MoneyData) => {
    if (!userHomeList) {
      console.error("ユーザーホームリストが未定義です");
      return;
    }
    // 編集されたデータを更新
    const updatedList = userHomeList.map((data) =>
      data.money_id === updatedData.money_id ? updatedData : data
    );
    setUserHomelist(updatedList);
    setIsEditModalOpen(false);
  };

  // 新規追加ボタン押下
  const handleAddMoney = () => {
    console.log("新規追加ボタンが押されました");
    setIsAddModalOpen(true);
  };

  // 新規保存の追加ボタン押下
  const handleAddMoneySave = (newData: MoneyData) => {
    if (!userHomeList) {
      setUserHomelist([newData]);
      setIsAddModalOpen(false);
      console.log("新しい" + userHomeList);
      return;
    } else {
      setUserHomelist([...userHomeList, newData]);
      setIsAddModalOpen(false);
      alert("新しい出費データを作成しました");
      console.log("追加データ" + userHomeList);
    }
  };

  const handleDeleteMoney = (Deletemoney: MoneyData) => {
    console.log("削除アイコンが押されました", Deletemoney);
    // 削除モーダルを開く
    setSelectData(Deletemoney);
    setIsDeleteModalOpen(true);
  };
  // ログアウト関数
  const logout = () => {
    sessionStorage.removeItem("user_id");
    sessionStorage.removeItem("nickname");
    navigate("/");
  };

  //カテゴリーフィルター
  const showUserData = selectedCategory
    ? userHomeList.filter((c) => c.category === selectedCategory)
    : userHomeList;

  // ユーザーデータを取得するためのuseEffect
  useEffect(() => {
    const user_id = sessionStorage.getItem("user_id");
    const nickname = sessionStorage.getItem("nickname");

    setNickname(nickname || "ゲスト");
    if (!user_id) {
      alert("ユーザーIDが見つかりません。ログインしてください。");
      logout();
      return;
    }
    console.log("ユーザーID:", user_id);
    const apiUrl = "http://localhost:8000/home_manager/view/" + user_id;
    axios
      .get(apiUrl)
      .then((response) => {
        if (response.status === 200) {
          if (response.data.length === 0) {
            console.log("データが存在しません");
            setUserHomelist([]);
          }
          setUserHomelist(response.data);
        } else {
          console.error("データの取得に失敗しました", response.status);
          alert("データの取得に失敗しました。再度ログインしてください。");
          logout();
        }
      })
      .catch((error) => {
        console.error("データの取得中にエラーが発生しました", error);
        alert(
          "データの取得中にエラーが発生しました。再度ログインしてください。"
        );
        logout();
      });
  }, []);
  return (
    <>
      <Header />
      <MdOutlineExitToApp
        className="logout-icon"
        onClick={() => logout()}
        size={50}
      />
      <h2>ようこそ、{nickname}さん</h2>
      <h3>最近の支出</h3>
      {/* userHomeListが存在していたら表示する */}
      <div className="home-space">
        {/* カテゴリーフィルター */}
        <CategoryFilter
          categorys={categorys}
          onCategoryChange={setSelectedCategory}
        />

        <div className="home-data">
          {showUserData && showUserData.length != 0 ? (
            // 支出データがある場合表示
            showUserData.map((moneyData, index) => (
              <div key={index}>
                <div className="home-box">
                  {/* 支出データの表示 */}
                  <h4>{moneyData.title}</h4>
                  {/* 編集ボタン */}
                  <FaPen
                    className="editbutton"
                    onClick={() => handleEditClick(moneyData)}
                  />
                  <p>金額: {moneyData.money}円</p>
                  <p>カテゴリー:{moneyData.category}</p>
                  <p>コメント: {moneyData.money_comment}</p>

                  {/* 削除ボタン */}
                  <FaTrash
                    className="trash-button"
                    onClick={() => handleDeleteMoney(moneyData)}
                  />
                </div>
              </div>
            ))
          ) : (
            // 支出データが存在しない場合
            <div> 支出データが存在しません </div>
          )}
        </div>
      </div>
      {/* 新規追加ボタン */}
      <IoIosAddCircle className="addbutton" onClick={() => handleAddMoney()} />
      {/* 編集モーダル */}
      <ModalModel
        isOpen={editModalIsOpen}
        onClose={() => setIsEditModalOpen(false)}
      >
        {selectedData && (
          <EditMoneyForm moneyData={selectedData} onSave={handleUpdateSave} />
        )}
      </ModalModel>
      {/* 新規追加モーダル */}
      <ModalModel
        isOpen={addModalIsOpen}
        onClose={() => setIsAddModalOpen(false)}
      >
        <AddMoneyForm
          moneyData={{
            money_id: 0, // 新規作成なので0に設定
            money: 0,
            category: "",
            title: "",
            money_comment: "",
          }}
          onSave={(newData) => handleAddMoneySave(newData)}
        />
      </ModalModel>

      {/* 出費データ削除確認 */}
      <ModalModel
        isOpen={deleteModalIsOpen}
        onClose={() => setIsDeleteModalOpen(false)}
      >
        {selectedData && (
          <DeleteModal
            moneyData={selectedData}
            onClose={() => setIsDeleteModalOpen(false)}
          />
        )}
      </ModalModel>
    </>
  );
};
export default Home;
