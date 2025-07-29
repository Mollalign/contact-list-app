import React from "react";

const ContactList = ({ contacts, updateContact, updateCallback }) => {
  const onDelete = async (id) => {
    try {
      const response = await fetch(`https://contact-manager-app-c5cd.onrender.com/delete_contact/${id}`, {
        method: "DELETE",
      });

      if (response.status === 200) {
        updateCallback();
      } else {
        console.error("Failed to delete");
      }
    } catch (error) {
      alert(error);
    }
  };

  return (
    <div className="p-4">
      <h2 className="text-2xl font-bold mb-4">Contacts</h2>

      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {contacts.map((contact) => (
          <div
            key={contact.id}
            className="bg-white rounded-2xl shadow-md p-4 hover:shadow-lg transition-all"
          >
            <div className="mb-2">
              <p className="text-lg font-semibold">
                {contact.firstName} {contact.lastName}
              </p>
              <p className="text-sm text-gray-600">{contact.email}</p>
            </div>

            <div className="flex justify-end gap-2 mt-4">
              <button
                onClick={() => updateContact(contact)}
                className="px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600 text-sm"
              >
                Update
              </button>
              <button
                onClick={() => onDelete(contact.id)}
                className="px-3 py-1 bg-red-500 text-white rounded hover:bg-red-600 text-sm"
              >
                Delete
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ContactList;
