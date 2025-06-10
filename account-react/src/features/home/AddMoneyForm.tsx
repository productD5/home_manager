import React from "react";
import { useState } from "react";

type AddMoneyFormProps = {
  moneyData: {
    money: number;
    category: string;
    title: string;
    money_comment: string;
  };
  onSave: (newData: AddMoneyFormProps["moneyData"]) => void;
};

const AddMoneyForm: React.FC<AddMoneyFormProps> = ({ moneyData, onSave }) => {
  const [formData, setFormData] = useState(moneyData);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault(); // フォームのデフォルトの送信動作を防ぐ(ページを再読み込みしない)
    onSave(formData); // 編集されたデータを親コンポーネントに渡す
    alert("新しい出費データを作成しました");
    setFormData({
      money: 0,
      category: "",
      title: "",
      money_comment: "",
    }); // フォームをリセット
  };
  return (
    <form onSubmit={handleSubmit}>
      <label>
        出費 :{" "}
        <input type="number" name="money" onChange={handleChange}></input>
      </label>
      <br />
      <label>
        カテゴリー :{" "}
        <input type="text" name="category" onChange={handleChange}></input>
      </label>
      <br />
      <label>
        タイトル :{" "}
        <input type="text" name="title" onChange={handleChange}></input>
      </label>
      <br />
      <label>
        コメント :{" "}
        <textarea name="money_comment" onChange={handleChange}></textarea>
      </label>
      <br />

      <button type="submit">新規追加</button>
    </form>
  );
};
export default AddMoneyForm;
