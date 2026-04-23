import React from 'react'
import colors from '../theme/Color'

const HeadingHere = ({ text, fontSize,width, fontWeight, ShowLine }) => {
    return (
        <>
            <div className='head_text_area'
                style={{
                    padding: '1% 0%'
                }}
            >
                <div className='head_text'
                    style={{
                        color: colors.secondary,
                        fontSize: fontSize ?? 16,
                        textTransform: 'capitalize',
                        fontWeight: fontWeight ?? 700
                    }}
                >
                    {text}
                </div>

                {ShowLine ? <div className='head_area_line'
                    style={{
                        position: 'relative',
                        left: 1,
                        height: 3,
                        width: width ?? '10%',
                        marginTop: 2,
                        backgroundColor: colors.success
                    }}
                ></div> : ''}
            </div>
        </>
    )
}

export default HeadingHere