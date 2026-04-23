import React, { useState, useEffect } from 'react';
import axios from 'axios';
import colors from '../../theme/Color';
import images from '../../images/Image';
import SmallButton from '../../components/SmallButton';
import HeadingHere from '../../components/HeadingHere';
import HeadBtn from '../../components/HeadBtn';

const ImportantAlerts = () => {
  const [text, setText] = useState('');
  const [alertId, setAlertId] = useState(null);

  // ===== GET alert =====
  const fetchAlert = async () => {
    try {
      const res = await axios.get('http://localhost:5000/api/alertnotices');
      if (res.data && res.data.length > 0) {
        setText(res.data[0].text);
        setAlertId(res.data[0]._id);
      } else {
        setText('');
        setAlertId(null);
      }
    } catch (err) {
      console.error('Fetch failed:', err);
    }
  };

  useEffect(() => {
    fetchAlert();
  }, []);

  // ===== ADD alert =====
  const handleAdd = async () => {
    if (!text.trim()) return alert('Please enter alert text.');
    try {
      await axios.post('http://localhost:5000/api/alertnotices', { text });
      alert('Alert added successfully');
      fetchAlert();
    } catch (err) {
      console.error(err);
      const backendMsg =
        err.response?.data?.message ||
        err.response?.data?.error ||
        'Add failed.';
      alert(backendMsg);
    }
  };


  // ===== UPDATE alert =====
  const handleUpdate = async () => {
    if (!alertId) return alert('No alert found to update.');
    try {
      await axios.put(`http://localhost:5000/api/alertnotices/${alertId}`, { text });
      alert('Alert updated successfully');
      fetchAlert();
    } catch (err) {
      const backendMsg = err.response?.data?.message || err.response?.data?.error || 'Update failed.';
      alert(backendMsg);

      alert('Update failed');
      console.error(err);
    }
  };

  // ===== DELETE alert =====
  const handleDelete = async () => {
    if (!alertId) return alert('No alert found to delete.');
    if (!window.confirm('Are you sure you want to delete this alert?')) return;
    try {
      await axios.delete(`http://localhost:5000/api/alertnotices/${alertId}`);
      alert('Alert deleted successfully');
      setText('');
      setAlertId(null);
    } catch (err) {
      const backendMsg = err.response?.data?.message || err.response?.data?.error || 'Delete failed.';
      alert(backendMsg);

      alert('Delete failed');
      console.error(err);
    }
  };

  return (
    <div
      className="image_area_here"
      style={{ backgroundImage: `url(${images.alert_bg})` }}
    >
      <div className="row_head_area">
        <HeadingHere
          text={'important alerts '}
          fontSize={16}
          ShowLine={true}
          width={'50%'}
        />

        {/* <SmallButton
          btn_text="delete"
          fontSize={9}
          width={55}
          justifyContent={'center'}
          backgroundColor={colors.danger}
          showbtnimg={false}
          onClick={handleDelete}
        /> */}

        {/* <SmallButton
          btn_text="add"
          fontSize={9}
          width={55}
          justifyContent={'center'}
          backgroundColor={colors.success}
          showbtnimg={false}
          onClick={handleAdd}
        /> */}

        <SmallButton
          btn_text="update"
          fontSize={9}
          width={55}
          justifyContent={'center'}
          backgroundColor={colors.success}
          showbtnimg={false}
          onClick={handleUpdate}
        />
      </div>

      <textarea
        className="inpt_alert_text"
        maxLength={180}
        style={{
          backgroundColor: 'transparent',
          resize: 'none',
          color: colors.secondary,
          outline: 'none',
          border: `1px solid ${colors.secondary}`,
        }}
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Enter alert text here..."
      />
    </div>
  );
};

export default ImportantAlerts;
