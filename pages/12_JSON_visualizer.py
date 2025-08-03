import streamlit as st
import json


def render_tree(data, level=0):
    indent = "&nbsp;" * 4 * level  # 4 spaces per level
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                st.markdown(f"{indent}📂 **{key}**")
                render_tree(value, level + 1)
            else:
                st.markdown(f"{indent}📄 **{key}**: `{value}`")
    elif isinstance(data, list):
        for index, item in enumerate(data):
            st.markdown(f"{indent}🔹 **[{index}]**")
            render_tree(item, level + 1)
    else:
        st.markdown(f"{indent}📄 `{data}`")


def main():
    st.title("🧬 JSON to Tree Diagram Visualizer")
    st.markdown("Paste your JSON below to explore it as a tree.")

    json_input = st.text_area("📥 JSON Input", height=300)

    if st.button("🔍 Visualize JSON"):
        try:
            json_data = json.loads(json_input)
            st.success("Valid JSON! Here's the tree view:")
            render_tree(json_data)
        except json.JSONDecodeError as e:
            st.error(f"Invalid JSON: {e}")

    st.markdown("---")
    if st.button("📄 Load Example JSON"):
        example = {
            "name": "Alice",
            "age": 30,
            "skills": ["Python", "Machine Learning"],
            "projects": {
                "2023": ["AI Assistant", "Stock Predictor"],
                "2024": ["Robotics"],
            },
        }
        st.session_state["example"] = json.dumps(example, indent=4)
        st.rerun()

    if "example" in st.session_state:
        st.text_area("📄 Example JSON", st.session_state["example"], height=300)


if __name__ == "__main__":
    main()
