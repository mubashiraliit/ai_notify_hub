import React, { useState, useEffect } from 'react';
import axios from 'axios';
import colors from '../../theme/Color';
import images from '../../images/Image';
import SmallButton from '../../components/SmallButton';
import HeadBtn from '../../components/HeadBtn';
import Modal from "react-modal";

const DepartmentTimetables = () => {
  const [timetables, setTimetables] = useState([]);
  const itemtables = [1, 2, 3, 4]

  const baseURL = 'http://localhost:5000/api/timetable';

  const [selectedTimetable, setSelectedTimetable] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleOpenModal = (item) => {
    console.log(item)
    setSelectedTimetable(item);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setSelectedTimetable(null);
  };

  // ✅ FETCH TIMETABLES
  const fetchTimetables = async () => {
    try {
      const res = await axios.get(baseURL);
      setTimetables(Array.isArray(res.data) ? res.data : []);
    } catch (err) {
      console.error('Fetch error:', err);
      setTimetables([]);
    }
  };

  useEffect(() => {
    fetchTimetables();
  }, []);


  const handleAddClick = () => {
    document.getElementById("timetableInput").click();
  };

  const handleAdd = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("image", file);

    try {
      await axios.post(`${baseURL}/upload`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      await fetchTimetables();
      alert("Timetable added successfully!");
    } catch (err) {
      console.error(err);
      const backendMsg =
        err.response?.data?.message ||
        err.response?.data?.error ||
        "Add failed.";
      alert(backendMsg);
    } finally {
      e.target.value = "";
    }
  };


  // ✅ UPDATE EXISTING
  const handleUpdate = async (id) => {
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = 'image/*';
    fileInput.onchange = async (e) => {
      const file = e.target.files[0];
      if (!file) return;
      const formData = new FormData();
      formData.append('image', file);
      try {
        await axios.put(`${baseURL}/${id}`, formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        });
        await fetchTimetables();
        alert('Timetable updated successfully!');
      } catch (err) {
        console.error(err);
        const backendMsg =
          err.response?.data?.message ||
          err.response?.data?.error ||
          'Update failed.';
        alert(backendMsg);
      }
    };
    fileInput.click();
  };

  // ✅ DELETE SINGLE
  const handleDelete = async (id) => {
    if (!window.confirm('Delete this timetable?')) return;
    try {
      await axios.delete(`${baseURL}/${id}`);
      await fetchTimetables();
      alert('Deleted successfully!');
    } catch (err) {
      console.error(err);
      const backendMsg =
        err.response?.data?.message ||
        err.response?.data?.error ||
        'Update failed.';
      alert(backendMsg);
    }
  };

  // ✅ DELETE ALL
  const handleDeleteAll = async () => {
    if (!window.confirm('Delete ALL timetables?')) return;
    try {
      await axios.delete(baseURL);
      await fetchTimetables();
      alert('All timetables deleted successfully!');
    } catch (err) {
      console.error(err);
      const backendMsg =
        err.response?.data?.message ||
        err.response?.data?.error ||
        'Update failed.';
      alert(backendMsg);
    }
  };

  // ✅ IMAGE URL
  const getImageUrl = (imgPath) =>
    imgPath ? `http://localhost:5000/${imgPath.replace(/\\/g, '/')}` : images.time_table;

  // ✅ DATE FORMATTER
  const formatDate = (dateStr) => {
    if (!dateStr) return '';
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-GB', {
      day: '2-digit',
      month: 'short',
      year: 'numeric',
    });
  };

  return (
    <div className="timetable_area" style={{ backgroundColor: colors.light_grey }}>
      {/* ---------- TOP BAR ---------- */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          // marginBottom: '10px',
        }}
      >
        <HeadBtn text={'Department Timetables'} width={'40%'} fontSize={16} />
        <>
          {/* ADD BUTTON */}
          {/* <div>
          <label
          htmlFor="addTimetableFile"
          style={{
            display: 'inline-block',
            padding: '6px 12px',
            backgroundColor: colors.secondary,
            color: '#fff',
            borderRadius: 6,
              cursor: 'pointer',
              fontSize: 13,
              }}
              >
              {loading ? 'Uploading...' : 'Add'}
          </label>
          <input
          id="addTimetableFile"
          type="file"
          accept="image/*"
          onChange={handleAdd}
            style={{ display: 'none' }}
          />
        </div> */}

          {/* DELETE ALL */}
          {/* <SmallButton
          btn_text="Delete All"
          backgroundColor={colors.danger || '#b22222'}
          onClick={handleDeleteAll}
          /> */}
        </>
      </div>

      {/* ---------- TIMETABLE LIST ---------- */}

      <div className="timetable_row_area">
        {/*     {timetables.length === 0 && (
          <p style={{ textAlign: 'center', color: colors.secondary, fontSize: 13 }}>
            No timetables found.
          </p>
        )}
        */}

        <>
          {timetables.map((item) => (
            <div
              key={item._id}
              className="timetable_here_outline"
              style={{ borderColor: colors.secondary, }}
            >
              <div
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  marginBottom: '2%',
                }}
              >
                <SmallButton
                  btn_text="Delete"
                  src={images.trash}
                  backgroundColor={colors.secondary}
                  onClick={() => handleDelete(item._id)}
                />
                <SmallButton
                  btn_text="Update"
                  src={images.editicon}
                  backgroundColor={colors.success}
                  onClick={() => handleUpdate(item._id)}
                />
              </div>

              <img
                onClick={() => handleOpenModal(item)}
                src={getImageUrl(item.image)}
                className="timetable_img_here"
                alt="timetable"
                style={{ borderColor: colors.secondary }}
              />
            </div>
          ))}

          {/* 👇🏽 Fill missing slots up to 4 total */}
          <input
            type="file"
            id="timetableInput"
            style={{ display: "none" }}
            onChange={handleAdd}
          />
          {Array.from({ length: 4 - timetables.length }, (_, index) => (
            console.log('timetables.image', timetables.image),
            <div
              key={`empty-${index}`}
              className="timetable_here_outline"
              style={{
                borderColor: colors.success,
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                cursor: 'pointer',
                height: 115,
                width: 180,
              }}
            >
              <img
                onClick={handleAddClick}
                src={images.add_image}
                // src={getImageUrl(timetables.image)}
                className="plus_image"
                alt="add timetable"
                style={{ borderColor: colors.success, width: 40, height: 40 }}
              />
            </div>
          ))}
        </>
        <Modal
          isOpen={isModalOpen}
          onRequestClose={handleCloseModal}
          contentLabel="Timetable Modal"
          style={{
            overlay: {
              backgroundColor: "rgba(0, 0, 0, 0.8)", // dim background
              zIndex: 9999,
            },
            content: {
              top: "50%",
              left: "50%",
              right: "auto",
              bottom: "auto",
              transform: "translate(-50%, -50%)",
              backgroundColor: colors.deep_grey,
              borderRadius: "10px",
              padding: "20px",
              border: "none",
              maxWidth: "90vw",
              maxHeight: "90vh",
            },
          }}
        >
          <div style={{ position: "relative" }}>
            <button
              onClick={handleCloseModal}
              style={{
                position: "absolute",
                top: 10,
                right: 10,
                background: colors.success,
                color: "#fff",
                border: "none",
                borderRadius: 5,
                padding: "5px 10px",
                cursor: "pointer",
              }}
            >
              ✕
            </button>

            {selectedTimetable && (
              <img
                // src={images.time_table}
                src={getImageUrl(selectedTimetable?.image)}
                alt="Full Timetable"
                style={{
                  width: "100%",
                  height: "auto",
                  borderRadius: 10,
                  border: `2px solid ${colors.success}`,
                }}
              />
            )}
          </div>
        </Modal>
      </div>
    </div>
  );
};

export default DepartmentTimetables;

{/* ✅ UPLOADED DATE */ }
{/* <p
              style={{
                textAlign: 'center',
                marginTop: 6,
                fontSize: 11,
                color: '#555',
                fontFamily: 'poppins',
              }}
            >
              Updated on: {formatDate(item.updatedAt)}

            </p> */}
