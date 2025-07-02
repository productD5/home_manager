import axios from "axios";
import React, { useState } from "react";

type EditProps = {
  moneyData: {
    money_id: number;
    money: number;
    category: string;
    title: string;
    money_comment: string;
  };
  // 編集フォームに渡すデータの型
  onSave: (updateData: EditProps["moneyData"]) => void;
};

const EditMoneyForm: React.FC<EditProps> = ({ moneyData, onSave }) => {
  const [formData, setFormData] = useState(moneyData);

  {
    /*フォームの値が変化したときに動作し値をformDataにコピーする関数*/
  }
  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault(); // フォームのデフォルトの送信動作を防ぐ(ページを再読み込みしない)

    const apiPath =
      "http://localhost:8000/home_manager/editMoney/" + moneyData.money_id;
    // APIにデータを送信
    console.log("APIパス:", apiPath);
    axios
      .put(apiPath, {
        money_id: moneyData.money_id,
        money: formData.money,
        category: formData.category,
        title: formData.title,
        money_comment: formData.money_comment,
      })
      .then((response) => {
        console.log("データが更新されました", response.data);
        onSave(formData); // 編集されたデータを親コンポーネントに渡す
      })
      .catch((error) => {
        console.error("データの更新に失敗しました", error);
      });
  };
  return (
    <form onSubmit={handleSubmit}>
      <label>
        出費 :{" "}
        <input
          type="number"
          name="money"
          value={formData.money}
          onChange={handleChange}
        ></input>
      </label>
      <br />
      <label>
        カテゴリー :{" "}
        <input
          type="text"
          name="category"
          value={formData.category}
          onChange={handleChange}
        ></input>
      </label>
      <br />
      <label>
        タイトル :{" "}
        <input
          type="text"
          name="title"
          value={formData.title}
          onChange={handleChange}
        ></input>
      </label>
      <br />
      <label>
        コメント :{" "}
        <textarea
          name="money_comment"
          value={formData.money_comment}
          onChange={handleChange}
        ></textarea>
      </label>
      <button type="submit">保存</button>
    </form>
  );
};
export default EditMoneyForm;
