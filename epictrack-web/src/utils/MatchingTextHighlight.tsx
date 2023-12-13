import { Palette } from "../styles/theme";


export const highlightText = (text: string, query: string) => {
  const index = text.toLowerCase().indexOf(query.toLowerCase());
  if (index !== -1) {
    return (
      <>
        {text.substring(0, index)}
        <span style={{ backgroundColor: Palette.secondary.main }}>
          {text.substring(index, index + query.length)}
        </span>
        {text.substring(index + query.length)}
      </>
    );
  }
  return text;
};
