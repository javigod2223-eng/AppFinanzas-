import streamlit as st
import pandas as pd
import math

# --- CONFIGURACIÓN GLOBAL ---
st.set_page_config(page_title="Sistema de Gestión Financiera", layout="wide")

# --- ESTILOS CSS CORPORATIVOS ---
st.markdown("""
    <style>
    .main { background-color: #f4f6f9; }
    h1, h2, h3 { font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #2c3e50; }
    h1 { font-size: 2.2rem; border-bottom: 2px solid #2c3e50; padding-bottom: 15px; }
    
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #dcdcdc;
        border-left: 5px solid #2c3e50;
        padding: 20px;
        border-radius: 4px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 15px;
    }
    .metric-card h3 { color: #2c3e50; font-size: 24px; margin: 0; font-weight: 700; }
    .metric-card p { color: #7f8c8d; font-size: 13px; margin-top: 5px; text-transform: uppercase; letter-spacing: 0.5px; }
    
    .metric-success {
        border-left: 5px solid #27ae60;
    }
    .metric-warning {
        border-left: 5px solid #f39c12;
    }
    .metric-danger {
        border-left: 5px solid #e74c3c;
    }
    
    .stButton>button {
        background-color: #34495e;
        color: white;
        border-radius: 4px;
        border: none;
        height: 3em;
        font-weight: 600;
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #2c3e50; }
    
    .stDataFrame { border: 1px solid #ddd; border-radius: 4px; }
    
    .info-box {
        background-color: #e8f4f8;
        border-left: 4px solid #3498db;
        padding: 15px;
        margin: 10px 0;
        border-radius: 4px;
    }
    
    .warning-box {
        background-color: #fef5e7;
        border-left: 4px solid #f39c12;
        padding: 15px;
        margin: 10px 0;
        border-radius: 4px;
    }
    
    .success-box {
        background-color: #e8f8f5;
        border-left: 4px solid #27ae60;
        padding: 15px;
        margin: 10px 0;
        border-radius: 4px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Sistema Integral de Presupuestos y Finanzas - 6NM62")

# --- MENÚ LATERAL ---
st.sidebar.header("Navegación")
modulo = st.sidebar.radio("Seleccione Módulo:", [
    "Inicio",
    "1. Presupuestos Operativos",
    "2. Análisis Financiero (Razones)",
    "3. Evaluación de Inversión"
])
st.sidebar.markdown("---")
st.sidebar.info("Versión Profesional 3.0 - Completo")

# ==============================================================================
#        MÓDULO 0: INICIO
# ==============================================================================
if modulo == "Inicio":
    st.markdown("#### Panel de Control Principal")
    st.write("Bienvenido al sistema. Seleccione una opción del menú lateral para proceder.")
    
    c1, c2, c3 = st.columns(3)
    c1.markdown("<div class='metric-card'><h3>Módulo 1</h3><p>Presupuestos Maestros</p></div>", unsafe_allow_html=True)
    c2.markdown("<div class='metric-card'><h3>Módulo 2</h3><p>Ratios Financieros</p></div>", unsafe_allow_html=True)
    c3.markdown("<div class='metric-card'><h3>Módulo 3</h3><p>Evaluación de Proyectos</p></div>", unsafe_allow_html=True)

# ==============================================================================
#        MÓDULO 1: PRESUPUESTOS OPERATIVOS (COMPLETO Y MEJORADO)
# ==============================================================================
elif modulo == "1. Presupuestos Operativos":
    st.header("🎯 Generador de Presupuestos Maestros")
    
    # Inicializar variables de sesión si no existen
    if 'datos_inicializados' not in st.session_state:
        st.session_state['datos_inicializados'] = True
        st.session_state['metodo_valuacion'] = 'UEPS'
    
    # Selector de método de valuación
    with st.expander("⚙️ Configuración del Sistema", expanded=False):
        st.session_state['metodo_valuacion'] = st.radio(
            "Método de Valuación de Inventarios:",
            ['UEPS', 'PEPS', 'Promedio Ponderado'],
            horizontal=True
        )
        st.info(f"📌 Método seleccionado: **{st.session_state['metodo_valuacion']}** - Este método se aplicará a todos los cálculos de inventarios.")
    
    tabs = st.tabs([
        "1️⃣ Ventas", 
        "2️⃣ Producción", 
        "3️⃣ Materiales", 
        "4️⃣ Mano de Obra", 
        "5️⃣ GIF",
        "6️⃣ Costo Producción",
        "7️⃣ Costo de Ventas",
        "8️⃣ Estado de Resultados"
    ])
    
    # ==================== TAB 1: VENTAS ====================
    with tabs[0]:
        st.subheader("📊 Presupuesto de Ventas")
        
        st.markdown("<div class='info-box'>💡 <b>Tip:</b> Este es el punto de partida de todo el presupuesto maestro.</div>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        unidades = c1.number_input("Unidades a vender", 0, 1000000, 63000, key="pv_uni", 
                                   help="Cantidad de productos que se planea vender en el período")
        precio = c2.number_input("Precio Unitario ($)", 0.0, 100000.0, 420.0, key="pv_precio",
                                 help="Precio de venta por unidad")
        
        ingreso = unidades * precio
        st.session_state['ventas_unidades'] = unidades
        st.session_state['ventas_precio'] = precio
        st.session_state['ventas_ingresos'] = ingreso
        
        st.markdown("---")
        st.markdown("### Resultado:")
        col1, col2, col3 = st.columns(3)
        col1.markdown(f"<div class='metric-card metric-success'><h3>{unidades:,}</h3><p>Unidades</p></div>", unsafe_allow_html=True)
        col2.markdown(f"<div class='metric-card'><h3>${precio:,.2f}</h3><p>Precio Unitario</p></div>", unsafe_allow_html=True)
        col3.markdown(f"<div class='metric-card metric-success'><h3>${ingreso:,.2f}</h3><p>Ingresos Totales</p></div>", unsafe_allow_html=True)

    # ==================== TAB 2: PRODUCCIÓN ====================
    with tabs[1]:
        st.subheader("🏭 Presupuesto de Producción")
        
        st.markdown("<div class='info-box'>💡 <b>Fórmula:</b> Unidades a Producir = Ventas + Inv. Final - Inv. Inicial</div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        v_est = col1.number_input("Ventas Estimadas", 
                                  value=st.session_state.get('ventas_unidades', 63000), 
                                  key="pp_ventas",
                                  help="Se toma del presupuesto de ventas")
        if_des = col2.number_input("Inventario Final Deseado", value=6000, key="pp_if",
                                   help="Inventario que queremos tener al final del período")
        ii_est = col3.number_input("Inventario Inicial", value=5000, key="pp_ii",
                                   help="Inventario con el que iniciamos el período")
        
        prod_req = v_est + if_des - ii_est
        st.session_state['prod_unidades'] = prod_req
        st.session_state['prod_inv_inicial_pt'] = ii_est
        st.session_state['prod_inv_final_pt'] = if_des
        
        st.markdown("---")
        st.markdown("### Cálculo:")
        
        df_prod = pd.DataFrame({
            'Concepto': [
                'Unidades a Vender',
                '(+) Inventario Final Deseado',
                '(=) Total Requerido',
                '(-) Inventario Inicial',
                '(=) UNIDADES A PRODUCIR'
            ],
            'Unidades': [v_est, if_des, v_est + if_des, ii_est, prod_req]
        })
        
        st.dataframe(df_prod.style.format({'Unidades': '{:,.0f}'}), hide_index=True, use_container_width=True)
        
        st.markdown(f"<div class='metric-card metric-success'><h3>{prod_req:,}</h3><p>Unidades a Producir</p></div>", unsafe_allow_html=True)

    # ==================== TAB 3: MATERIALES (CON VALUACIÓN) ====================
    with tabs[2]:
        st.subheader("📦 Presupuesto de Requerimientos y Compras de Materiales")
        
        st.markdown("### Paso 1: Requerimientos de Materia Prima")
        st.markdown("<div class='info-box'>💡 Calcula cuánta materia prima necesitas para la producción planeada</div>", unsafe_allow_html=True)
        
        # Materiales A y B
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔹 Material A")
            prod = st.number_input("Producción Requerida", 
                                  value=st.session_state.get('prod_unidades', 64000), 
                                  key="pm_prod_a", disabled=True)
            std_mat_a = st.number_input("Piezas de Material A por Unidad", value=7.0, key="pm_std_a",
                                       help="Cuántas piezas de Material A necesita cada producto")
            req_total_a = prod * std_mat_a
            st.metric("Requerimiento Total Material A", f"{req_total_a:,.0f} piezas")
            
        with col2:
            st.markdown("#### 🔹 Material B")
            st.number_input("Producción Requerida", 
                           value=st.session_state.get('prod_unidades', 64000), 
                           key="pm_prod_b", disabled=True)
            std_mat_b = st.number_input("Piezas de Material B por Unidad", value=3.0, key="pm_std_b",
                                       help="Cuántas piezas de Material B necesita cada producto")
            req_total_b = prod * std_mat_b
            st.metric("Requerimiento Total Material B", f"{req_total_b:,.0f} piezas")
        
        st.markdown("---")
        st.markdown("### Paso 2: Presupuesto de Compras")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔹 Material A")
            ii_mat_a = st.number_input("Inventario Inicial (piezas)", value=40000.0, key="pm_ii_a")
            precio_ii_a = st.number_input("Precio Unit. Inv. Inicial ($)", value=5.0, key="pm_precio_ii_a")
            if_mat_a = st.number_input("Inventario Final Deseado (piezas)", value=35000.0, key="pm_if_a")
            costo_mat_a = st.number_input("Precio de Compra Actual ($)", value=6.0, key="pm_costo_a")
            
            compras_uni_a = req_total_a + if_mat_a - ii_mat_a
            costo_compras_a = compras_uni_a * costo_mat_a
            
            st.markdown(f"""
            <div class='success-box'>
                <b>📋 Resumen Material A:</b><br>
                • Necesario para producción: {req_total_a:,.0f}<br>
                • (+) Inv. Final: {if_mat_a:,.0f}<br>
                • (-) Inv. Inicial: {ii_mat_a:,.0f}<br>
                • = <b>A Comprar: {compras_uni_a:,.0f} piezas</b><br>
                • <b>Costo: ${costo_compras_a:,.2f}</b>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("#### 🔹 Material B")
            ii_mat_b = st.number_input("Inventario Inicial (piezas)", value=15000.0, key="pm_ii_b")
            precio_ii_b = st.number_input("Precio Unit. Inv. Inicial ($)", value=11.0, key="pm_precio_ii_b")
            if_mat_b = st.number_input("Inventario Final Deseado (piezas)", value=12000.0, key="pm_if_b")
            costo_mat_b = st.number_input("Precio de Compra Actual ($)", value=12.0, key="pm_costo_b")
            
            compras_uni_b = req_total_b + if_mat_b - ii_mat_b
            costo_compras_b = compras_uni_b * costo_mat_b
            
            st.markdown(f"""
            <div class='success-box'>
                <b>📋 Resumen Material B:</b><br>
                • Necesario para producción: {req_total_b:,.0f}<br>
                • (+) Inv. Final: {if_mat_b:,.0f}<br>
                • (-) Inv. Inicial: {ii_mat_b:,.0f}<br>
                • = <b>A Comprar: {compras_uni_b:,.0f} piezas</b><br>
                • <b>Costo: ${costo_compras_b:,.2f}</b>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### Paso 3: Valuación de Inventarios")
        st.markdown(f"<div class='warning-box'>⚙️ <b>Método aplicado: {st.session_state['metodo_valuacion']}</b></div>", unsafe_allow_html=True)
        
        # Función para calcular valuación según método
        def calcular_valuacion(inv_inicial, precio_inicial, compras, precio_compras, consumo, metodo):
            total_disponible = inv_inicial + compras
            
            if metodo == 'UEPS':
                # Primero sale lo último que entró (compras)
                if consumo <= compras:
                    costo_consumo = consumo * precio_compras
                    inv_final_cant = total_disponible - consumo
                    # El inventario final es del inicial
                    costo_inv_final = inv_final_cant * precio_inicial
                else:
                    # Se consumen todas las compras y parte del inicial
                    costo_consumo = (compras * precio_compras) + ((consumo - compras) * precio_inicial)
                    inv_final_cant = total_disponible - consumo
                    costo_inv_final = inv_final_cant * precio_inicial
                    
            elif metodo == 'PEPS':
                # Primero sale lo primero que entró (inicial)
                if consumo <= inv_inicial:
                    costo_consumo = consumo * precio_inicial
                    inv_final_cant = total_disponible - consumo
                    # Inventario final viene de compras
                    costo_inv_final = inv_final_cant * precio_compras
                else:
                    # Se consume todo el inicial y parte de compras
                    costo_consumo = (inv_inicial * precio_inicial) + ((consumo - inv_inicial) * precio_compras)
                    inv_final_cant = total_disponible - consumo
                    costo_inv_final = inv_final_cant * precio_compras
                    
            else:  # Promedio Ponderado
                valor_total = (inv_inicial * precio_inicial) + (compras * precio_compras)
                costo_promedio = valor_total / total_disponible
                costo_consumo = consumo * costo_promedio
                inv_final_cant = total_disponible - consumo
                costo_inv_final = inv_final_cant * costo_promedio
            
            return costo_consumo, costo_inv_final, inv_final_cant
        
        # Calcular Material A
        costo_consumo_a, costo_inv_final_a, cant_inv_final_a = calcular_valuacion(
            ii_mat_a, precio_ii_a, compras_uni_a, costo_mat_a, req_total_a, st.session_state['metodo_valuacion']
        )
        
        # Calcular Material B
        costo_consumo_b, costo_inv_final_b, cant_inv_final_b = calcular_valuacion(
            ii_mat_b, precio_ii_b, compras_uni_b, costo_mat_b, req_total_b, st.session_state['metodo_valuacion']
        )
        
        # Guardar en sesión
        st.session_state['mp_costo_produccion_a'] = costo_consumo_a
        st.session_state['mp_costo_produccion_b'] = costo_consumo_b
        st.session_state['mp_total_produccion'] = costo_consumo_a + costo_consumo_b
        
        # Mostrar resultados
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔹 Material A")
            st.markdown(f"""
            <div class='metric-card'>
                <h3>${costo_consumo_a:,.2f}</h3>
                <p>Costo MP A en Producción</p>
            </div>
            """, unsafe_allow_html=True)
            st.info(f"Inventario Final: {cant_inv_final_a:,.0f} piezas = ${costo_inv_final_a:,.2f}")
            
        with col2:
            st.markdown("#### 🔹 Material B")
            st.markdown(f"""
            <div class='metric-card'>
                <h3>${costo_consumo_b:,.2f}</h3>
                <p>Costo MP B en Producción</p>
            </div>
            """, unsafe_allow_html=True)
            st.info(f"Inventario Final: {cant_inv_final_b:,.0f} piezas = ${costo_inv_final_b:,.2f}")
        
        st.markdown(f"""
        <div class='metric-card metric-success'>
            <h3>${costo_consumo_a + costo_consumo_b:,.2f}</h3>
            <p>Costo Total de Materia Prima en Producción</p>
        </div>
        """, unsafe_allow_html=True)

    # ==================== TAB 4: MANO DE OBRA ====================
    with tabs[3]:
        st.subheader("👷 Presupuesto de Mano de Obra Directa (MOD)")
        
        st.markdown("<div class='info-box'>💡 <b>Fórmula:</b> Costo MOD = Unidades × Horas/Unidad × Tarifa/Hora</div>", unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        mod_prod = c1.number_input("Producción Requerida", 
                                   value=st.session_state.get('prod_unidades', 64000), 
                                   key="mod_prod", disabled=True)
        hrs_unit = c2.number_input("Horas por Unidad", value=13.0, key="mod_hrs",
                                   help="Horas de trabajo requeridas para producir una unidad")
        cuota_hr = c3.number_input("Tarifa por Hora ($)", value=9.0, key="mod_costo",
                                   help="Salario por hora del trabajador directo")
        
        total_horas = mod_prod * hrs_unit
        costo_mod = total_horas * cuota_hr
        
        st.session_state['mod_costo_total'] = costo_mod
        
        st.markdown("---")
        st.markdown("### Resultado:")
        
        col1, col2, col3 = st.columns(3)
        col1.markdown(f"<div class='metric-card'><h3>{total_horas:,.0f}</h3><p>Total de Horas</p></div>", unsafe_allow_html=True)
        col2.markdown(f"<div class='metric-card'><h3>${cuota_hr:,.2f}</h3><p>Tarifa por Hora</p></div>", unsafe_allow_html=True)
        col3.markdown(f"<div class='metric-card metric-success'><h3>${costo_mod:,.2f}</h3><p>Costo Total MOD</p></div>", unsafe_allow_html=True)

    # ==================== TAB 5: GASTOS INDIRECTOS DE FABRICACIÓN ====================
    with tabs[4]:
        st.subheader("🏭 Presupuesto de Gastos Indirectos de Fabricación (GIF)")
        
        st.markdown("<div class='info-box'>💡 Los GIF incluyen todos los costos de fabricación que no son materia prima directa ni mano de obra directa</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            mat_indirecto = st.number_input("Material Indirecto", value=1320000.0, key="gif_mat",
                                           help="Materiales auxiliares, lubricantes, suministros, etc.")
            moi = st.number_input("Mano de Obra Indirecta", value=2130000.0, key="gif_moi",
                                 help="Supervisores, almacenistas, control de calidad, etc.")
            renta = st.number_input("Renta de Planta", value=360000.0, key="gif_renta",
                                   help="Arrendamiento o depreciación de instalaciones")
        
        with col2:
            energia = st.number_input("Energía Eléctrica", value=464000.0, key="gif_energia",
                                     help="Luz, gas, agua de la planta")
            mantenimiento = st.number_input("Mantenimiento", value=674000.0, key="gif_mant",
                                           help="Reparaciones y mantenimiento preventivo")
            varios = st.number_input("Gastos Varios", value=500000.0, key="gif_varios",
                                    help="Seguros, impuestos prediales, otros gastos")
        
        total_gif = mat_indirecto + moi + renta + energia + mantenimiento + varios
        st.session_state['gif_total'] = total_gif
        
        st.markdown("---")
        st.markdown("### Resumen de GIF:")
        
        df_gif = pd.DataFrame({
            'Concepto': ['Material Indirecto', 'Mano de Obra Indirecta', 'Renta', 
                        'Energía', 'Mantenimiento', 'Varios', 'TOTAL'],
            'Importe': [mat_indirecto, moi, renta, energia, mantenimiento, varios, total_gif]
        })
        
        st.dataframe(df_gif.style.format({'Importe': '${:,.2f}'}).apply(
            lambda x: ['background-color: #e8f8f5; font-weight: bold' if x.name == len(df_gif)-1 else '' for i in x], axis=1
        ), hide_index=True, use_container_width=True)
        
        st.markdown(f"<div class='metric-card metric-success'><h3>${total_gif:,.2f}</h3><p>Total Gastos Indirectos de Fabricación</p></div>", unsafe_allow_html=True)

    # ==================== TAB 6: COSTO DE PRODUCCIÓN ====================
    with tabs[5]:
        st.subheader("💰 Cédula de Costo de Producción")
        
        st.markdown("<div class='info-box'>💡 <b>Costo de Producción = Materia Prima + MOD + GIF</b></div>", unsafe_allow_html=True)
        
        # Recuperar datos
        mp_total = st.session_state.get('mp_total_produccion', 0)
        mod_total = st.session_state.get('mod_costo_total', 0)
        gif_total = st.session_state.get('gif_total', 0)
        unidades_prod = st.session_state.get('prod_unidades', 1)
        
        # Validación
        if mp_total == 0 or mod_total == 0 or gif_total == 0:
            st.warning("⚠️ Completa las pestañas anteriores para ver el costo de producción")
        else:
            costo_total_prod = mp_total + mod_total + gif_total
            costo_unitario = costo_total_prod / unidades_prod if unidades_prod > 0 else 0
            
            st.session_state['costo_produccion_total'] = costo_total_prod
            st.session_state['costo_unitario'] = costo_unitario
            
            # Tabla resumen
            df_costo = pd.DataFrame({
                'Concepto': ['Materia Prima Directa', 'Mano de Obra Directa', 
                            'Gastos Indirectos de Fabricación', 'COSTO TOTAL DE PRODUCCIÓN'],
                'Importe': [mp_total, mod_total, gif_total, costo_total_prod]
            })
            
            st.dataframe(df_costo.style.format({'Importe': '${:,.2f}'}).apply(
                lambda x: ['background-color: #e8f8f5; font-weight: bold' if x.name == len(df_costo)-1 else '' for i in x], axis=1
            ), hide_index=True, use_container_width=True)
            
            st.markdown("---")
            st.markdown("### Resultados:")
            
            col1, col2, col3 = st.columns(3)
            col1.markdown(f"<div class='metric-card metric-success'><h3>${costo_total_prod:,.2f}</h3><p>Costo Total de Producción</p></div>", unsafe_allow_html=True)
            col2.markdown(f"<div class='metric-card'><h3>{unidades_prod:,}</h3><p>Unidades Producidas</p></div>", unsafe_allow_html=True)
            col3.markdown(f"<div class='metric-card metric-success'><h3>${costo_unitario:,.2f}</h3><p>Costo Unitario</p></div>", unsafe_allow_html=True)

    # ==================== TAB 7: COSTO DE VENTAS (CONTINUACIÓN) ====================
    with tabs[6]:
        st.subheader("🛒 Presupuesto de Costo de Ventas")
        
        st.markdown(f"<div class='warning-box'>⚙️ <b>Método de valuación: {st.session_state['metodo_valuacion']}</b></div>", unsafe_allow_html=True)
        
        # Inputs
        col1, col2 = st.columns(2)
        inv_inicial_pt = col1.number_input("Inventario Inicial PT (unidades)", 
                                          value=st.session_state.get('prod_inv_inicial_pt', 5000), 
                                          key="cv_ii")
        precio_inv_inicial_pt = col2.number_input("Costo Unit. Inv. Inicial PT", value=250.0, key="cv_precio_ii",
                                                  help="Costo unitario del inventario inicial de producto terminado")
        
        # Datos de producción
        unidades_producidas = st.session_state.get('prod_unidades', 64000)
        costo_unit_prod = st.session_state.get('costo_unitario', 279.27)
        unidades_vendidas = st.session_state.get('ventas_unidades', 63000)
        inv_final_pt = st.session_state.get('prod_inv_final_pt', 6000)
        
        # Validación
        if costo_unit_prod == 0:
            st.warning("⚠️ Completa la pestaña de Costo de Producción primero")
        else:
            # Calcular disponible
            total_disponible = inv_inicial_pt + unidades_producidas
            valor_inv_inicial = inv_inicial_pt * precio_inv_inicial_pt
            valor_produccion = unidades_producidas * costo_unit_prod
            valor_total_disponible = valor_inv_inicial + valor_produccion
            
            # Calcular según método de valuación
            if st.session_state['metodo_valuacion'] == 'UEPS':
                # Primero sale lo último que entró (producción)
                if unidades_vendidas <= unidades_producidas:
                    costo_ventas = unidades_vendidas * costo_unit_prod
                    # Inv final es del inicial
                    valor_inv_final = inv_final_pt * precio_inv_inicial_pt
                else:
                    # Se vende toda la producción y parte del inicial
                    costo_ventas = (unidades_producidas * costo_unit_prod) + ((unidades_vendidas - unidades_producidas) * precio_inv_inicial_pt)
                    valor_inv_final = inv_final_pt * precio_inv_inicial_pt
                    
            elif st.session_state['metodo_valuacion'] == 'PEPS':
                # Primero sale lo primero (inicial)
                if unidades_vendidas <= inv_inicial_pt:
                    costo_ventas = unidades_vendidas * precio_inv_inicial_pt
                    # Inv final viene de producción
                    valor_inv_final = inv_final_pt * costo_unit_prod
                else:
                    # Se vende todo el inicial y parte de producción
                    costo_ventas = (inv_inicial_pt * precio_inv_inicial_pt) + ((unidades_vendidas - inv_inicial_pt) * costo_unit_prod)
                    valor_inv_final = inv_final_pt * costo_unit_prod
                    
            else:  # Promedio Ponderado
                costo_promedio = valor_total_disponible / total_disponible
                costo_ventas = unidades_vendidas * costo_promedio
                valor_inv_final = inv_final_pt * costo_promedio
            
            st.session_state['costo_ventas'] = costo_ventas
            st.session_state['valor_inv_final_pt'] = valor_inv_final
            
            # Mostrar tabla de valuación
            st.markdown("### Valuación de Producto Terminado:")
            
            df_valuacion_pt = pd.DataFrame({
                'Concepto': ['Inventario Inicial', 'Producción del Período', 'Total Disponible', 
                            'Inventario Final', 'COSTO DE VENTAS'],
                'Unidades': [inv_inicial_pt, unidades_producidas, total_disponible, 
                            inv_final_pt, unidades_vendidas],
                'Costo Unitario': [precio_inv_inicial_pt, costo_unit_prod, '-', 
                                  '-', '-'],
                'Importe': [valor_inv_inicial, valor_produccion, valor_total_disponible, 
                           valor_inv_final, costo_ventas]
            })
            
            st.dataframe(df_valuacion_pt.style.format({
                'Unidades': '{:,.0f}',
                'Costo Unitario': lambda x: '${:,.2f}'.format(x) if isinstance(x, (int, float)) else x,
                'Importe': '${:,.2f}'
            }).apply(
                lambda x: ['background-color: #e8f8f5; font-weight: bold' if x.name == len(df_valuacion_pt)-1 else '' for i in x], axis=1
            ), hide_index=True, use_container_width=True)
            
            st.markdown("---")
            
            # Desglose según método
            st.markdown("### Composición del Costo de Ventas:")
            
            if st.session_state['metodo_valuacion'] == 'UEPS':
                if unidades_vendidas <= unidades_producidas:
                    st.markdown(f"""
                    <div class='info-box'>
                        <b>Aplicando UEPS (Últimas Entradas, Primeras Salidas):</b><br>
                        • Se vendieron {unidades_vendidas:,} unidades<br>
                        • Todas provienen de la producción actual<br>
                        • {unidades_vendidas:,} unidades × ${costo_unit_prod:,.2f} = <b>${costo_ventas:,.2f}</b>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    unidades_del_inicial = unidades_vendidas - unidades_producidas
                    st.markdown(f"""
                    <div class='info-box'>
                        <b>Aplicando UEPS (Últimas Entradas, Primeras Salidas):</b><br>
                        • Toda la producción: {unidades_producidas:,} × ${costo_unit_prod:,.2f} = ${unidades_producidas * costo_unit_prod:,.2f}<br>
                        • Del inventario inicial: {unidades_del_inicial:,} × ${precio_inv_inicial_pt:,.2f} = ${unidades_del_inicial * precio_inv_inicial_pt:,.2f}<br>
                        • <b>Total Costo de Ventas: ${costo_ventas:,.2f}</b>
                    </div>
                    """, unsafe_allow_html=True)
            
            elif st.session_state['metodo_valuacion'] == 'PEPS':
                if unidades_vendidas <= inv_inicial_pt:
                    st.markdown(f"""
                    <div class='info-box'>
                        <b>Aplicando PEPS (Primeras Entradas, Primeras Salidas):</b><br>
                        • Se vendieron {unidades_vendidas:,} unidades<br>
                        • Todas provienen del inventario inicial<br>
                        • {unidades_vendidas:,} unidades × ${precio_inv_inicial_pt:,.2f} = <b>${costo_ventas:,.2f}</b>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    unidades_de_produccion = unidades_vendidas - inv_inicial_pt
                    st.markdown(f"""
                    <div class='info-box'>
                        <b>Aplicando PEPS (Primeras Entradas, Primeras Salidas):</b><br>
                        • Todo el inv. inicial: {inv_inicial_pt:,} × ${precio_inv_inicial_pt:,.2f} = ${inv_inicial_pt * precio_inv_inicial_pt:,.2f}<br>
                        • De la producción: {unidades_de_produccion:,} × ${costo_unit_prod:,.2f} = ${unidades_de_produccion * costo_unit_prod:,.2f}<br>
                        • <b>Total Costo de Ventas: ${costo_ventas:,.2f}</b>
                    </div>
                    """, unsafe_allow_html=True)
            
            else:  # Promedio
                costo_prom = valor_total_disponible / total_disponible
                st.markdown(f"""
                <div class='info-box'>
                    <b>Aplicando Promedio Ponderado:</b><br>
                    • Costo Promedio = ${valor_total_disponible:,.2f} ÷ {total_disponible:,} = ${costo_prom:,.2f}<br>
                    • Costo de Ventas = {unidades_vendidas:,} × ${costo_prom:,.2f} = <b>${costo_ventas:,.2f}</b>
                </div>
                """, unsafe_allow_html=True)
            
            # Métricas finales
            col1, col2, col3 = st.columns(3)
            col1.markdown(f"<div class='metric-card metric-danger'><h3>${costo_ventas:,.2f}</h3><p>Costo de Ventas</p></div>", unsafe_allow_html=True)
            col2.markdown(f"<div class='metric-card'><h3>{unidades_vendidas:,}</h3><p>Unidades Vendidas</p></div>", unsafe_allow_html=True)
            col3.markdown(f"<div class='metric-card'><h3>${valor_inv_final:,.2f}</h3><p>Valor Inv. Final PT</p></div>", unsafe_allow_html=True)

    # ==================== TAB 8: ESTADO DE RESULTADOS ====================
    with tabs[7]:
        st.subheader("📊 Estado de Resultados Presupuestado")
        
        st.markdown("<div class='info-box'>💡 <b>Estado Financiero que muestra la utilidad o pérdida del período</b></div>", unsafe_allow_html=True)
        
        # Sección de Gastos de Operación
        with st.expander("💼 Gastos de Operación", expanded=True):
            st.markdown("#### Ingrese los Gastos de Operación:")
            
            col1, col2 = st.columns(2)
            
            with col1:
                comisiones = st.number_input("Comisiones a Vendedores", value=2750000.0, key="go_comisiones",
                                            help="Comisiones pagadas al equipo de ventas")
                sueldos = st.number_input("Sueldos Administrativos", value=1820000.0, key="go_sueldos",
                                         help="Sueldos del personal administrativo")
                publicidad = st.number_input("Publicidad", value=670000.0, key="go_publicidad",
                                            help="Gastos de marketing y publicidad")
            
            with col2:
                servicios = st.number_input("Servicios", value=580000.0, key="go_servicios",
                                           help="Servicios profesionales, legales, contables, etc.")
                diversos = st.number_input("Gastos Diversos", value=1200000.0, key="go_diversos",
                                          help="Otros gastos operativos")
            
            total_gastos_op = comisiones + sueldos + publicidad + servicios + diversos
            st.session_state['gastos_operacion'] = total_gastos_op
            
            # Tabla de gastos
            df_gastos = pd.DataFrame({
                'Concepto': ['Comisiones a Vendedores', 'Sueldos', 'Publicidad', 
                            'Servicios', 'Diversos', 'TOTAL GASTOS DE OPERACIÓN'],
                'Importe': [comisiones, sueldos, publicidad, servicios, diversos, total_gastos_op]
            })
            
            st.dataframe(df_gastos.style.format({'Importe': '${:,.2f}'}).apply(
                lambda x: ['background-color: #fef5e7; font-weight: bold' if x.name == len(df_gastos)-1 else '' for i in x], axis=1
            ), hide_index=True, use_container_width=True)
        
        st.markdown("---")
        
        # Recuperar todos los datos necesarios
        ingresos = st.session_state.get('ventas_ingresos', 0)
        costo_ventas = st.session_state.get('costo_ventas', 0)
        gastos_op = st.session_state.get('gastos_operacion', 0)
        
        # Validación
        if ingresos == 0 or costo_ventas == 0:
            st.warning("⚠️ Completa todas las pestañas anteriores para ver el Estado de Resultados completo")
        else:
            # Cálculos
            utilidad_bruta = ingresos - costo_ventas
            utilidad_operativa = utilidad_bruta - gastos_op
            
            # Guardar en sesión
            st.session_state['utilidad_bruta'] = utilidad_bruta
            st.session_state['utilidad_operativa'] = utilidad_operativa
            
            # Estado de Resultados
            st.markdown("### Estado de Resultados Presupuestado:")
            
            df_edo_resultados = pd.DataFrame({
                'Concepto': [
                    'VENTAS',
                    '(-) COSTO DE VENTAS',
                    '(=) UTILIDAD BRUTA',
                    '(-) GASTOS DE OPERACIÓN',
                    '(=) UTILIDAD OPERATIVA'
                ],
                'Importe': [
                    ingresos,
                    costo_ventas,
                    utilidad_bruta,
                    gastos_op,
                    utilidad_operativa
                ]
            })
            
            # Aplicar estilos
            def aplicar_estilo(row):
                if row.name == 0:  # Ventas
                    return ['background-color: #e8f8f5; font-weight: bold'] * len(row)
                elif row.name == 2:  # Utilidad Bruta
                    return ['background-color: #e8f4f8; font-weight: bold'] * len(row)
                elif row.name == 4:  # Utilidad Operativa
                    return ['background-color: #d5f4e6; font-weight: bold; font-size: 16px'] * len(row)
                else:
                    return [''] * len(row)
            
            st.dataframe(df_edo_resultados.style.format({
                'Importe': '${:,.2f}'
            }).apply(aplicar_estilo, axis=1), hide_index=True, use_container_width=True)
            
            st.markdown("---")
            
            # Métricas clave
            st.markdown("### 📈 Indicadores Clave:")
            
            col1, col2, col3, col4 = st.columns(4)
            
            margen_bruto = (utilidad_bruta / ingresos * 100) if ingresos > 0 else 0
            margen_operativo = (utilidad_operativa / ingresos * 100) if ingresos > 0 else 0
            
            col1.markdown(f"<div class='metric-card metric-success'><h3>${ingresos:,.2f}</h3><p>Ventas Totales</p></div>", unsafe_allow_html=True)
            col2.markdown(f"<div class='metric-card metric-warning'><h3>${utilidad_bruta:,.2f}</h3><p>Utilidad Bruta</p></div>", unsafe_allow_html=True)
            col3.markdown(f"<div class='metric-card metric-success'><h3>${utilidad_operativa:,.2f}</h3><p>Utilidad Operativa</p></div>", unsafe_allow_html=True)
            col4.markdown(f"<div class='metric-card'><h3>{margen_operativo:.2f}%</h3><p>Margen Operativo</p></div>", unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Análisis adicional
            st.markdown("### 💡 Análisis de Márgenes:")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div class='success-box'>
                    <b>Margen Bruto:</b> {margen_bruto:.2f}%<br>
                    <small>Por cada $100 de ventas, $  {margen_bruto:.2f} quedan después de cubrir el costo de ventas</small>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class='success-box'>
                    <b>Margen Operativo:</b> {margen_operativo:.2f}%<br>
                    <small>Por cada $100 de ventas, ${margen_operativo:.2f} quedan como utilidad operativa</small>
                </div>
                """, unsafe_allow_html=True)
            
            # Botón de descarga
            st.markdown("---")
            
            # Crear resumen completo para descarga
            resumen_completo = f"""
ESTADO DE RESULTADOS PRESUPUESTADO
COMPAÑÍA XZ, S.A.
{'='*60}

VENTAS                           ${ingresos:>20,.2f}
(-) COSTO DE VENTAS              ${costo_ventas:>20,.2f}
                                 {'-'*30}
(=) UTILIDAD BRUTA               ${utilidad_bruta:>20,.2f}

(-) GASTOS DE OPERACIÓN:
    Comisiones                   ${comisiones:>20,.2f}
    Sueldos                      ${sueldos:>20,.2f}
    Publicidad                   ${publicidad:>20,.2f}
    Servicios                    ${servicios:>20,.2f}
    Diversos                     ${diversos:>20,.2f}
                                 {'-'*30}
    Total Gastos de Operación    ${gastos_op:>20,.2f}

(=) UTILIDAD OPERATIVA           ${utilidad_operativa:>20,.2f}

{'='*60}
INDICADORES:
Margen Bruto:       {margen_bruto:>6.2f}%
Margen Operativo:   {margen_operativo:>6.2f}%
            """
            
            st.download_button(
                label="📥 Descargar Estado de Resultados",
                data=resumen_completo,
                file_name="estado_resultados_presupuestado.txt",
                mime="text/plain"
            )

# ==============================================================================
#        MÓDULO 2: ANÁLISIS FINANCIERO (RAZONES)
# ==============================================================================
elif modulo == "2. Análisis Financiero (Razones)":
    st.header("📊 Análisis de Razones Financieras")
    st.info("🚧 Módulo en desarrollo - Próximamente disponible")
    
    st.markdown("""
    Este módulo incluirá:
    - Razones de Liquidez
    - Razones de Rentabilidad
    - Razones de Endeudamiento
    - Razones de Actividad
    """)

# ==============================================================================
#        MÓDULO 3: EVALUACIÓN DE INVERSIÓN
# ==============================================================================
elif modulo == "3. Evaluación de Inversión":
    st.header("💼 Evaluación de Proyectos de Inversión")
    st.info("🚧 Módulo en desarrollo - Próximamente disponible")
    
    st.markdown("""
    Este módulo incluirá:
    - Valor Presente Neto (VPN)
    - Tasa Interna de Retorno (TIR)
    - Período de Recuperación
    - Índice de Rentabilidad

    """)
