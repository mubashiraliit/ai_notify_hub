import React, { useEffect, useState, useRef } from 'react';
import axios from 'axios';
import colors from '../../theme/Color';
import images from '../../images/Image';
import SmallButton from '../../components/SmallButton';
import ButtonHere from '../../components/ButtonHere';
import HeadBtn from '../../components/HeadBtn';
import Modal from "react-modal";


const AcademicNotices = () => {
  const items = [1, 2];
  const [notices, setNotices] = useState([]);
  const [loadingUpload, setLoadingUpload] = useState(false);
  const updateInputRef = useRef(null);
  const [selectedTimetable, setSelectedTimetable] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [updateId, setUpdateId] = useState(null);

  const handleOpenModal = (item) => {
    setSelectedTimetable(item);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setSelectedTimetable(null);
  };

  const fetchNotices = async () => {
    try {
      const res = await axios.get('http://localhost:5000/api/notices/');
      if (Array.isArray(res.data)) setNotices(res.data);
      else if (res.data?.events) setNotices(res.data.events);
      else if (res.data?.data?.events) setNotices(res.data.data.events);
      else setNotices([]);
    } catch (err) {
      console.error('Error fetching notices:', err);
      setNotices([]);
    }
  };

  useEffect(() => {
    fetchNotices();
  }, []);

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const formData = new FormData();
    formData.append('image', file);

    try {
      setLoadingUpload(true);
      await axios.post('http://localhost:5000/api/notices/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      await fetchNotices();
      alert('Image uploaded successfully!');
    } catch (err) {
      console.error(err);
      const backendMsg =
        err.response?.data?.message ||
        err.response?.data?.error ||
        'Add failed.';
      alert(backendMsg);
    } finally {
      setLoadingUpload(false);
      e.target.value = '';
    }
  };

  // ✅ Update fix (file picker properly triggers)
  const handleUpdate = (id) => {
    console.log(id)
    setUpdateId(id);
    updateInputRef.current?.click();
  };

  const onUpdateFileSelected = async (e) => {
    const file = e.target.files[0];
    if (!file || !updateId) return;
    const formData = new FormData();
    formData.append('image', file);

    try {
      await axios.put(`http://localhost:5000/api/notices/${updateId}`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      await fetchNotices();
      alert('Notice updated successfully!');
    } catch (err) {
      console.error('Update failed:', err);
      alert('Update failed.');
    } finally {
      e.target.value = '';
      setUpdateId(null);
    }
  };

  // ✅ Delete fix
  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this notice?')) return;
    try {
      const res = await axios.delete(`http://localhost:5000/api/notices/${id}`);
      if (res.status === 200 || res.status === 204) {
        alert('Notice deleted successfully!');
        await fetchNotices();
      } else {
        alert('Delete failed: unexpected response.');
      }
    } catch (err) {
      console.error('Delete error:', err);
      alert('Delete failed.');
    }
  };

  const getImageUrl = (imgPath) =>
    imgPath ? `http://localhost:5000/${imgPath.replace(/\\/g, '/')}` : null;

  return (
    <div className="down_notice_area" style={{ backgroundColor: colors.light_grey }}>
      <div className="btn_area">
        <ButtonHere btn_text={'academic notices'} />
      </div>

      <div className="responsive_area">
        <HeadBtn text={'department Notices '} width={'50%'} fontSize={16} />
      </div>

      <div className="sub_notice_area">
        {/* --- Actual Notices --- */}
        {notices.map((noticeObj, index) => (
          <div
            key={`notice-${noticeObj._id || index}`}
            className="notice_here_outline"
            style={{
              borderColor: colors.success,
              position: 'relative', // ✅ Important for z-index isolation
              zIndex: 5, // ✅ make sure buttons are clickable
            }}
          >
            <div
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                marginBottom: '4%',
                zIndex: 10,
                position: 'relative', // ✅ keeps button layer on top
              }}
            >
              <SmallButton
                btn_text="delete"
                backgroundColor={colors.secondary}
                onClick={() => handleDelete(noticeObj._id)}
              />
              <SmallButton
                btn_text="update"
                onClick={() => handleUpdate(noticeObj._id)}
              />
            </div>

            <div>
              <img
                onClick={() => handleOpenModal(noticeObj)}
                src={getImageUrl(noticeObj.image)}
                className="notice_here"
                alt="notice"
                style={{
                  borderColor: colors.success,
                  zIndex: 1,
                  position: 'relative',
                }}
              />
            </div>
          </div>
        ))}

        {/* --- Placeholder Boxes (for missing notices) --- */}
        {/* Hidden file input */}
        <input
          type="file"
          id="notice-upload"
          accept="image/*"
          style={{ display: "none" }}
          onChange={handleUpload}
        />

        {Array.from({ length: Math.max(0, 2 - notices.length) }).map((_, index) => (
          <div
            key={`placeholder-${index}`}
            className="notice_here_outline"
            style={{
              borderColor: colors.success,
              backgroundColor: '#f2f2f2',
              display: 'flex',
              justifyContent: 'center',
              alignItems: 'center',
              position: 'relative',
              zIndex: 1,
              cursor: 'pointer',
            }}
            onClick={() => document.getElementById('notice-upload').click()} // ✅ trigger input
          >
            <img
              src={images.add_image}
              alt="add notice"
              style={{
                width: 80,
                height: 80,
                opacity: 0.7,
                objectFit: 'contain',
              }}
            />
          </div>
        ))}

      </div>

      {/* MODAL */}
      <Modal
        isOpen={isModalOpen}
        onRequestClose={handleCloseModal}
        contentLabel="Timetable Modal"
        style={{
          overlay: {
            backgroundColor: "rgba(0, 0, 0, 0.8)",
            zIndex: 9999,
          },
          content: {
            top: "48%",
            left: "50%",
            right: "auto",
            bottom: "auto",
            transform: "translate(-50%, -50%)",
            backgroundColor: colors.deep_grey,
            borderRadius: "10px",
            padding: "20px",
            border: "none",
            maxWidth: "30%",
            maxHeight: "80vh",
          },
        }}
      >
        <div
          style={{
            position: "relative",
            display: "flex",
            justifyContent: "center",
          }}
        >
          <button
            onClick={handleCloseModal}
            style={{
              position: "absolute",
              top: -10,
              right: '.1%',
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
              src={`http://localhost:5000/${selectedTimetable.image.replace("\\", "/")}`}
              alt="Full timetable"
              style={{
                display: "flex",
                alignSelf: "center",
                width: "80%",
                height: "auto",
                borderRadius: 10,
                border: `2px solid ${colors.success}`,
              }}
            />
          )}
        </div>
      </Modal>

      <>
        <div style={{ padding: '8px 12px', display: 'flex', justifyContent: 'center', display: 'none' }}>

          <label
            htmlFor="addNoticeFile"
            style={{
              display: 'inline-block',
              padding: '6px 12px',
              backgroundColor: '#8a1d2c',
              color: '#fff',
              borderRadius: 6,
              cursor: 'pointer',
              fontSize: 13,
              boxShadow: '0 1px 0 rgba(0,0,0,0.1)',
            }}
            title="Add Notice Image"
          >
            {loadingUpload ? 'Uploading...' : 'Add'}
          </label>
          <input
            id="addNoticeFile"
            type="file"
            accept="image/*"
            onChange={handleUpload}
            style={{ display: 'none' }}
          />
          <input
            ref={updateInputRef}
            type="file"
            accept="image/*"
            onChange={onUpdateFileSelected}
            style={{ display: 'none' }}
          />
        </div>
      </>

    </div>
  );
};

export default AcademicNotices;
