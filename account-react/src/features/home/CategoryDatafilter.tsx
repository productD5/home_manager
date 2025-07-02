import React from "react";
type CategoryfilterProps = {
  categorys: string[];
  onCategoryChange: (category: string) => void;
};

const CategoryFilter: React.FC<CategoryfilterProps> = ({
  categorys,
  onCategoryChange,
}) => {
  return (
    <select onChange={(e) => onCategoryChange(e.target.value)}>
      <option value="">すべて表示</option>
      {categorys.map((cat) => (
        <option key={cat} value={cat}>
          {cat}
        </option>
      ))}
    </select>
  );
};
export default CategoryFilter;
