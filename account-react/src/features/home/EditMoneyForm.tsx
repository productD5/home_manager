import React, { useState } from "react";

type EditProps = {
  moneyData: {
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
    onSave(formData); // 編集されたデータを親コンポーネントに渡す
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
