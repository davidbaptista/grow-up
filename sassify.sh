for i in static/css/*.scss; do
    rm ${i%.*}.css
    sassc $i >> "${i%.*}.css"
done
