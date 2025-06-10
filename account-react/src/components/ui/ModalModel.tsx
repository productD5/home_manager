import React from "react";
import "@/components/styles/modalModel.css";

type ModalModelProps = {
  isOpen: boolean;
  onClose: () => void;
  children: React.ReactNode;
};
const ModalModel: React.FC<ModalModelProps> = ({
  isOpen,
  onClose,
  children,
}) => {
  if (!isOpen) return null;
  return (
    <div className="modal-overlay">
      <div className="modal-content" onClick={(e) => e.stopPropagation}>
        <button className="modal-close" onClick={onClose}>
          x
        </button>
        {children}
      </div>
    </div>
  );
};
export default ModalModel;
