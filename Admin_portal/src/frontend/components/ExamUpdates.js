import React, { useState, useEffect } from 'react';
import axios from 'axios';
import colors from '../../theme/Color';
import SmallButton from '../../components/SmallButton';
import HeadingHere from '../../components/HeadingHere';

const ExamUpdates = () => {
  const [examText, setExamText] = useState('');
  const [examId, setExamId] = useState(null);

  // ✅ Fetch latest exam date
  const fetchExamDate = async () => {
    try {
      const res = await axios.get('http://localhost:5000/api/exam-dates');
      const data = res.data?.[0]; // since response is an array
      if (data) {
        setExamText(data.date || '');
        setExamId(data._id || null);
      } else {
        setExamText('');
        setExamId(null);
      }
    } catch (err) {
      console.error('Fetch error:', err);
      alert('Failed to fetch exam date.');
    }
  };

  useEffect(() => {
    fetchExamDate();
  }, []);

  // ✅ Add exam date
  const handleAdd = async () => {
    if (!examText.trim()) return alert('Please enter an exam date.');
    try {
      const res = await axios.post('http://localhost:5000/api/exam-dates', { date: examText });
      alert(res.data?.message || 'Exam date added successfully.');
      fetchExamDate();
    } catch (err) {
      console.error('Add error:', err);
      alert(err.response?.data?.message || 'Add failed.');
    }
  };

  // ✅ Update exam date
  const handleUpdate = async () => {
    if (!examId) return alert('No exam date found to update.');
    try {
      const res = await axios.put(`http://localhost:5000/api/exam-dates/${examId}`, {
        date: examText,
      });
      alert(res.data?.message || 'Exam date updated successfully.');
      fetchExamDate();
    } catch (err) {
      console.error('Update error:', err);
      alert(err.response?.data?.message || 'Update failed.');
    }
  };

  // ✅ Delete exam date
  const handleDelete = async () => {
    if (!examId) return alert('No exam date found to delete.');
    try {
      const res = await axios.delete(`http://localhost:5000/api/exam-dates/${examId}`);
      alert(res.data?.message || 'Exam date deleted successfully.');
      fetchExamDate();
    } catch (err) {
      console.error('Delete error:', err);
      alert(err.response?.data?.message || 'Delete failed.');
    }
  };

  return (
    <div className="main_btn_area" style={{ backgroundColor: colors.light_grey }}>
      <div className="btn_area_mid_term">
        <div className="row_head_area">
          <HeadingHere text={'Exams updates'} ShowLine={true} fontSize={12} width={'50%'} />

          <div style={{ display: 'flex', gap: 6 }}>
            {/* <SmallButton
              btn_text="add"
              fontSize={9}
              width={45}
              justifyContent="center"
              backgroundColor={colors.success}
              showbtnimg={false}
              onClick={handleAdd}
            /> */}
            <SmallButton
              btn_text="update"
              fontSize={9}
              width={55}
              justifyContent="center"
              backgroundColor={colors.success}
              showbtnimg={false}
              onClick={handleUpdate}
            />
            {/* <SmallButton
              btn_text="delete"
              fontSize={9}
              width={55}
              justifyContent="center"
              backgroundColor={colors.danger}
              showbtnimg={false}
              onClick={handleDelete}
            /> */}
          </div>
        </div>

        <input
          type="text"
          value={examText}
          onChange={(e) => setExamText(e.target.value)}
          maxLength={34}
          className="mid_term_inpt"
          style={{ outline: 'none', border: `1px solid ${colors.success}` }}
        />
      </div>
    </div>
  );
};

export default ExamUpdates;
