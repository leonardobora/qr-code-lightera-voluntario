import pandas as pd
import plotly.graph_objects as go

data = [
    {"Architecture Type": "Simple Static Website", "Complexity": "Baixa", "Development Time": "2-3 dias", "Cost": "Gratuito", "Maintenance": "Mínima", "Scalability": "Limitada"},
    {"Architecture Type": "Single-Page App (SPA)", "Complexity": "Baixa-Média", "Development Time": "1 semana", "Cost": "Gratuito", "Maintenance": "Baixa", "Scalability": "Média"},
    {"Architecture Type": "Flask/Python Backend", "Complexity": "Média", "Development Time": "1-2 semanas", "Cost": "$5-25/mês", "Maintenance": "Média", "Scalability": "Boa"},
    {"Architecture Type": "Database + API", "Complexity": "Média-Alta", "Development Time": "2-3 semanas", "Cost": "$15-50/mês", "Maintenance": "Alta", "Scalability": "Muito Boa"},
    {"Architecture Type": "Full Event Management System", "Complexity": "Alta", "Development Time": "1-2 meses", "Cost": "$50+/mês", "Maintenance": "Muito Alta", "Scalability": "Excelente"}
]

df = pd.DataFrame(data)

header_vals = [
    "Arch. Type", "Complexity", "Dev. Time", "Cost", "Maint.", "Scalability"
]
cell_vals = [
    [
        "Static Website", "SPA", "Flask/Py Backend", "DB + API", "Event Mgmt Sys"
    ],
    [
        "Baixa", "Baixa-Média", "Média", "Média-Alta", "Alta"
    ],
    [
        "2-3 dias", "1 semana", "1-2 sem.", "2-3 sem.", "1-2 meses"
    ],
    [
        "Gratuito", "Gratuito", "$5-25/mês", "$15-50/mês", "$50+/mês"
    ],
    [
        "Mínima", "Baixa", "Média", "Alta", "Muito Alta"
    ],
    [
        "Limitada", "Média", "Boa", "Muito Boa", "Excelente"
    ]
]

# Create alternating row colors for readability
row_colors = []
color1 = '#F0FBFC'  # very light cyan
color2 = '#FFFFFF'  # white
for i in range(len(cell_vals[0])):
    row_colors.append(color1 if i%2 == 0 else color2)
cell_fill = [row_colors for _ in range(len(header_vals))]

fig = go.Figure(data=[go.Table(
    header=dict(
        values=header_vals,
        align='center',
        fill_color='#1FB8CD',
        font=dict(size=16, color='white'),
        height=45
    ),
    cells=dict(
        values=cell_vals,
        align='center',
        fill_color=cell_fill,
        font=dict(size=15, color='black'),
        height=38
    )
)])

fig.update_layout(
    title=dict(text="Architecture Option Compare", x=0.5, font=dict(size=23)),
)

fig.write_image("qr_arch_table_final.png")
