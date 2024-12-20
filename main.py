import streamlit as st

def main():
    st.title("Análisis de Empresa")
    
    # Inputs
    company_name = st.text_input("Nombre de la empresa")
    company_context = st.text_area("Contexto de la empresa")
    impressions = st.number_input("Impresiones", min_value=0, step=1)
    clicks = st.number_input("Clicks", min_value=0, step=1)
    actions = st.text_input("Acciones (separadas por coma)")
    
    # Process
    if st.button("Obtener Resultado"):
        if company_name and company_context and actions:
            st.success(f"La empresa {company_name}, tuvo {clicks} clicks y {impressions} impresiones, y se realizaron estas acciones: {actions}")
        else:
            st.error("Por favor, complete todos los campos para obtener el resultado.")

if __name__ == "__main__":
    main()
