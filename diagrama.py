def generate_mxgraph_model():
    mxgraph_model = '''<mxGraphModel dx="106237" dy="61883" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="0" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169" math="0" shadow="0">
  <root>
    <mxCell id="0" />
    <mxCell id="1" parent="0" />
    <mxCell id="2" value="Головна (Main Page)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
      <mxGeometry x="100" y="100" width="160" height="40" as="geometry" />
    </mxCell>
    <mxCell id="3" value="Про нас (About Us)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
      <mxGeometry x="100" y="200" width="160" height="40" as="geometry" />
    </mxCell>
    <mxCell id="4" value="Список курортів (List of Resorts)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
      <mxGeometry x="100" y="300" width="160" height="40" as="geometry" />
    </mxCell>
    <mxCell id="5" value="Деталі курорту (Resort Details)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
      <mxGeometry x="300" y="300" width="160" height="40" as="geometry" />
    </mxCell>
    <mxCell id="6" value="Реєстрація (Registration)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
      <mxGeometry x="100" y="400" width="160" height="40" as="geometry" />
    </mxCell>
    <mxCell id="7" value="Вхід (Login)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
      <mxGeometry x="100" y="500" width="160" height="40" as="geometry" />
    </mxCell>
    <mxCell id="8" value="Адмін-панель (Admin Panel)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
      <mxGeometry x="100" y="600" width="160" height="40" as="geometry" />
    </mxCell>
    <mxCell id="9" value="Додати курорти (Add Resorts)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
      <mxGeometry x="300" y="600" width="160" height="40" as="geometry" />
    </mxCell>
    <mxCell id="10" value="Перегляд бронювань (View Bookings)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
      <mxGeometry x="300" y="700" width="160" height="40" as="geometry" />
    </mxCell>
    <mxCell id="11" value="Статистика (Statistics)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
      <mxGeometry x="300" y="800" width="160 ```python
      <mxGeometry x="300" y="800" width="160" height="40" as="geometry" />
    </mxCell>
    
    <!-- Стрілки -->
    <mxCell id="12" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;endArrow=none;" edge="1" parent="1" source="2" target="3" />
    <mxCell id="13" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;endArrow=none;" edge="1" parent="1" source="2" target="4" />
    <mxCell id="14" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;endArrow=none;" edge="1" parent="1" source="2" target="6" />
    <mxCell id="15" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;endArrow=none;" edge="1" parent="1" source="2" target="7" />
    <mxCell id="16" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;endArrow=none;" edge="1" parent="1" source="4" target="5" />
    <mxCell id="17" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;endArrow=none;" edge="1" parent="1" source="8" target="9" />
    <mxCell id="18" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;endArrow=none;" edge="1" parent="1" source="8" target="10" />
    <mxCell id="19" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;endArrow=none;" edge="1" parent="1" source="8" target="11" />
  </root>
</mxGraphModel>'''
    return mxgraph_model

# Виклик функції та виведення результату
print(generate_mxgraph_model())