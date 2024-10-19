import React, { useState } from "react";

// Type definition for the dropdown options (sub-items) and their descriptions
type DropdownItem = {
  label: string;
  value: string;
  description: string;
};

type ListItem = {
  id: number;
  name: string;
  dropdownItems: DropdownItem[];
};

interface ListWithDropdownProps {
  items: ListItem[];
}

const ListWithDropdown: React.FC<ListWithDropdownProps> = ({ items }) => {
  // State to track which main list item is expanded (clicked)
  const [expandedItemId, setExpandedItemId] = useState<number | null>(null);

  // State to track the currently selected sub-item
  const [selectedSubItemValue, setSelectedSubItemValue] = useState<string | null>(null);

  // Toggle the expanded state of the list item
  const toggleItem = (itemId: number) => {
    setExpandedItemId((prevItemId) => (prevItemId === itemId ? null : itemId));
    setSelectedSubItemValue(null); // Reset sub-item selection when switching main list item
  };

  // Handle sub-item click and ensure only one description is shown at a time
  const toggleSubItemDescription = (subItemValue: string) => {
    setSelectedSubItemValue((prevValue) => (prevValue === subItemValue ? null : subItemValue));
  };

  return (
    <div>
      {items.map((item) => (
        <div key={item.id} style={{ marginBottom: "20px" }}>
          {/* Main list item clickable */}
          <h3
            onClick={() => toggleItem(item.id)}
            style={{ cursor: "pointer", userSelect: "none" }}
          >
            {item.name}
          </h3>

          {/* Sub-items are shown if the main item is clicked */}
          {expandedItemId === item.id && (
            <ul>
              {item.dropdownItems.map((dropdownItem) => (
                <li key={dropdownItem.value}>
                  <span
                    onClick={() => toggleSubItemDescription(dropdownItem.value)}
                    style={{ cursor: "pointer", textDecoration: "underline", userSelect: "none" }}
                  >
                    {dropdownItem.label}
                  </span>

                  {/* Description is shown if this sub-item is selected */}
                  {selectedSubItemValue === dropdownItem.value && (
                    <p style={{ marginLeft: "20px", color: "gray" }}>
                      {dropdownItem.description}
                    </p>
                  )}
                </li>
              ))}
            </ul>
          )}
        </div>
      ))}
    </div>
  );
};

// Example usage
const App: React.FC = () => {
  const listItems: ListItem[] = [
    {
      id: 1,
      name: "Item 1",
      dropdownItems: [
        { label: "Option 1", value: "option1", description: "This is the description for Option 1" },
        { label: "Option 2", value: "option2", description: "This is the description for Option 2" },
      ],
    },
    {
      id: 2,
      name: "Item 2",
      dropdownItems: [
        { label: "Option A", value: "optionA", description: "This is the description for Option A" },
        { label: "Option B", value: "optionB", description: "This is the description for Option B" },
      ],
    },
  ];

  return <ListWithDropdown items={listItems} />;
};

export default App;
