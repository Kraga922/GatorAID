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
  const [selectedSubItemValue, setSelectedSubItemValue] = useState<
    string | null
  >(null);

  // Toggle the expanded state of the list item
  const toggleItem = (itemId: number) => {
    setExpandedItemId((prevItemId) => (prevItemId === itemId ? null : itemId));
    setSelectedSubItemValue(null); // Reset sub-item selection when switching main list item
  };

  // Handle sub-item click and ensure only one description is shown at a time
  const toggleSubItemDescription = (subItemValue: string) => {
    setSelectedSubItemValue((prevValue) =>
      prevValue === subItemValue ? null : subItemValue
    );
  };

  return (
    <div>
      {items.map((item) => (
        <div key={item.id} style={{ marginBottom: "20px" }}>
          {/* Main list item clickable */}
          <h3
            onClick={() => toggleItem(item.id)}
            style={{ cursor: "pointer", userSelect: "none" }}
            className="text"
          >
            {item.name}
          </h3>

          {/* Sub-items are shown if the main item is clicked */}
          {expandedItemId === item.id && (
            <ul className="text">
              {item.dropdownItems.map((dropdownItem) => (
                <li key={dropdownItem.value} className="bulletpoint">
                  <span
                    onClick={() => toggleSubItemDescription(dropdownItem.value)}
                    style={{
                      cursor: "pointer",
                      textDecoration: "underline",
                      userSelect: "none",
                    }}
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
const Menu: React.FC = () => {
  const listItems: ListItem[] = [
    {
      id: 1,
      name: "Shoulder",
      dropdownItems: [
        {
          label: "Arm Swing",
          value: "option1",
          description:
            "Move your arm in a circular motion perpendicular to the ground.",
        },
        {
          label: "Lateral Raises",
          value: "option2",
          description:
            "Lift your arms straight out to the sides until shoulder level. Then, lower them back down.",
        },
        {
          label: "Shoulder Press",
          value: "option3",
          description:
            "Press weights overhead from shoulder height. Then, lower back to starting position.",
        },
      ],
    },
    {
      id: 2,
      name: "Knee",
      dropdownItems: [
        {
          label: "Quad-Stretch",
          value: "option1",
          description:
            "Stand on one leg. Pull the opposite heal towards your buttocks, and hold for a stretch.",
        },
        {
          label: "Squats",
          value: "option2",
          description:
            "Lower your body by bending your knees and hips. Then, return to standing position.",
        },
        {
          label: "Hamstring Curl",
          value: "option3",
          description:
            "Bend your knee to lift your heel to a 90-degree angle, then lower back down.",
        },
      ],
    },
    {
      id: 3,
      name: "Arms",
      dropdownItems: [
        {
          label: "Bicep Curl",
          value: "optionA",
          description:
            "Lift weights towards your shoulders by bending your elbows. Then, lower back down.",
        },
      ],
    },
  ];

  return <ListWithDropdown items={listItems} />;
};

export default Menu;
