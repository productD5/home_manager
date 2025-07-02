import axios from "axios";
import "@/components/styles/deletemodal.css";

type DeleteModelProps = {
  moneyData: {
    money_id: number;
  };
  onClose: () => void;
};

const DeleteModal: React.FC<DeleteModelProps> = ({ moneyData, onClose }) => {
  const handledelete = () => {
    const apiPath =
      "http://localhost:8000/home_manager/deleteMoney/" + moneyData.money_id;

    try {
      axios.delete(apiPath);
    } catch (error) {
      console.log("支出データの削除に失敗しました:" + error);
    }
    window.location.reload();
  };
  return (
    <div>
      <h2>データを削除しますか？</h2>
      <button className="Yesbutton" onClick={() => handledelete()}>
        はい
      </button>

      <button className="Nobutton" onClick={onClose}>
        いいえ
      </button>
    </div>
  );
};

export default DeleteModal;
