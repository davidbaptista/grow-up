for i in static/css/*.scss; do
    sassc $i >> "${i%.*}.css"
done
