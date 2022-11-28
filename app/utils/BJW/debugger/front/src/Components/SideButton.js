import React, {useState} from "react";
import styled from "styled-components";

const ButtonDiv = styled.div`
    color: white;
    display: flex;
    flex-direction: row;
    align-items: center;
    background-color: black;
    
    
    padding: 2rem, 0;
    margin: 10px;
    top: 5rem;
    margin-left: 0;
    
    width: ${(props) => (props.hover? "12rem" : "3.5rem")};
    transition: all 0.5s ease;border-radius: 0 30px 30px 0;
`;

const Img = styled.img`
    display: flex;
    width: 2rem;
    height: auto;
    margin: 3px;
    
    object-fit: cover;
    
    filter: ${(props) => (
        props.hover
        ? "invert(76%) sepia(11%) saturate(310%) hue-rotate(162deg) brightness(99%) contrast(88%)"
        : "invert(76%) sepia(11%) saturate(310%) hue-rotate(162deg) brightness(72%) contrast(88%)"
    )}
`;

const Span = styled.span`
    display: flex;
    margin-left: 3rem;
`;

export default ({image, value}) => {
    const [isHovering, setIsHovering] = useState(false);
    const handleHovering = () => setIsHovering(!isHovering)

    return (
        <ButtonDiv
            hover={isHovering}
            onMouseEnter={() => handleHovering()}
            onMouseLeave={() => handleHovering()}
        >
            <Img hover={isHovering} src={image} alt={value}/>
            {isHovering &&
                <Span>{value}</Span>
            }
        </ButtonDiv>
    )
}