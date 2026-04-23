import React, { useState, useEffect } from 'react';
import colors from '../../theme/Color';
import SmallButton from '../../components/SmallButton';
import HeadingHere from '../../components/HeadingHere';

const StudentAIFAQs = () => {
  const [faqs, setFaqs] = useState([]);
  const [newQuestion, setNewQuestion] = useState('');

  const API_URL = 'http://localhost:5000/api/chatbot';

  const fetchFaqs = async () => {
    try {
      const res = await fetch(API_URL);
      const data = await res.json();
      setFaqs(data);
    } catch (err) {
      console.error('Failed to fetch questions:', err);
    }
  };

  const handleAdd = async () => {
    if (!newQuestion.trim()) return alert('Question text required');
    try {
      const res = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ questions: newQuestion }),
      });
      const data = await res.json();
      if (res.ok) {
        setNewQuestion('');
        fetchFaqs();
      } else alert(data.message || 'Failed to add question.');
    } catch (err) {
      console.error('Add failed:', err);
    }
  };

  const handleUpdate = async (id, updatedText) => {
    try {
      const res = await fetch(`${API_URL}/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ questions: updatedText }),
      });
      const data = await res.json();
      if (res.ok) fetchFaqs();
      else alert(data.message || 'Failed to update question.');
    } catch (err) {
      console.error('Update failed:', err);
    }
  };

  const handleDelete = async (id) => {
    try {
      const res = await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
      const data = await res.json();
      if (res.ok) fetchFaqs();
      else alert(data.message || 'Failed to delete question.');
    } catch (err) {
      console.error('Delete failed:', err);
    }
  };

  const handleDeleteAll = async () => {
    if (!window.confirm('Are you sure to delete all questions?')) return;
    try {
      const res = await fetch(API_URL, { method: 'DELETE' });
      const data = await res.json();
      if (res.ok) fetchFaqs();
      else alert(data.message || 'Failed to delete all questions.');
    } catch (err) {
      console.error('Delete all failed:', err);
    }
  };

  useEffect(() => {
    fetchFaqs();
  }, []);

  return (
    <div
      className="ai_keyword_area"
      style={{ borderRadius: 10, /* padding: '1%' */ }}
    >
      {/* ✅ Heading and top buttons */}
      {/* <div
        className="row_head_area"
        style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}
      > */}
        {/* <HeadingHere text={'AI assistant'} ShowLine={true} fontSize={12} width={'35%'} /> */}

        {/* <div style={{ display: 'flex', gap: 10 }}> */}
          {/* <SmallButton
            btn_text="update"
            fontSize={9}
            width={50}
            justifyContent="center"
            backgroundColor={colors.success}
            showbtnimg={false} */}
          {/* // onClick={handleAdd} */}
          {/* /> */}
        {/* </div> */}
      {/* </div> */}

      {/* ✅ Add new question input */}
      {/* <div style={{ margin: '10px 2% 20px 2%' }}>
        <textarea
          type="text"
          defaultValue={ "this AI is built for provide the answers under the circumstances. This AI is designed to provide accurate and instant answers related to academic needs. Whether it’s about classes, teacher timetables, or departmental updates, feel free to ask and get the information you need right away."
          }
          value={newQuestion}
          onChange={(e) => setNewQuestion(e.target.value)}
          // rows={3}
          style={{
            // width: 'calc(100% - 12px)',
            // padding: '6px 10px',
            // backgroundColor: 'transparent',
            // boxSizing: 'border-box',
            color:colors.secondary,
            border: `1px solid ${colors.success}`,
            outline: 'none',
            borderRadius: 5,
            fontSize: 11,
          }}
        />
      </div> */}
      {/* <div style={{ padding: '2% 5%', marginTop: '.1%' }} className='faq_area_down'>

        <textarea rows={6} className='point_hightlights' type='text'
          style={{
            color: colors.black, outline: 'none', border: `1px solid ${colors.success}`, resize: 'none',
            backgroundColor: 'transparent', width: '98%', margin: ".1% 0%", borderRadius: 5, fontSize: 10,
            fontFamily: 'poppins', textTransform: 'capitalize', padding: '2% 2%',
            lineHeight: 1.9
          }}
          disabled={true}
          defaultValue={"this AI is built for provide the answers under the circumstances. This AI is designed to provide accurate and instant answers related to academic needs. Whether it’s about classes, teacher timetables, or departmental updates, feel free to ask and get the information you need right away."}
          maxLength={290} /> */}
        {/* // value={newQuestion} */}
        {/* // onChange={(e) => setNewQuestion(e.target.value)} */}
      {/* </div> */}
    </div>
  );
};

export default StudentAIFAQs;
