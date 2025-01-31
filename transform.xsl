name: Convert XML to Markdown
on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  convert:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout source repository
        uses: actions/checkout@v4

      - name: Set up JDK
        uses: actions/setup-java@v4
        with:
          java-version: '11'
          distribution: 'temurin'

      - name: Checkout DocusaurusWebsite repository
        uses: actions/checkout@v4
        with:
          repository: Pantagrueliste/CavrianaCorr_FrontEnd
          path: CavrianaCorr_FrontEnd
          token: ${{ secrets.DOCUSAURUS_REPO_SECRET }}

      - name: Download Saxon and XML Resolver
        run: |
          wget -O saxon.jar https://repo1.maven.org/maven2/net/sf/saxon/Saxon-HE/10.6/Saxon-HE-10.6.jar
          wget -O xml-resolver.jar https://repo1.maven.org/maven2/xml-resolver/xml-resolver/1.2/xml-resolver-1.2.jar

      - name: Create docs/letters directory
        run: |
          mkdir -p CavrianaCorr_FrontEnd/docs/letters

      - name: Convert XML to Markdown by Year
        run: |
          for file in ./letters/*.xml; do
            if [[ "$file" != "./letters/persNames.xml" && "$file" != "./letters/placeNames.xml" ]]; then
              if [ -f "$file" ]; then
                filename=$(basename -- "$file")
                year=$(
                  java -cp saxon.jar:xml-resolver.jar net.sf.saxon.Query \
                  -qs:"declare namespace tei='http://www.tei-c.org/ns/1.0'; substring(doc('$file')/tei:TEI/tei:teiHeader/tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/tei:date/@when,1,4)" \
                  2>/dev/null
                )
                if [ -z "$year" ]; then
                  year="unknownYear"
                fi
                mkdir -p "CavrianaCorr_FrontEnd/docs/letters/$year"
                output_file="CavrianaCorr_FrontEnd/docs/letters/$year/${filename%.*}.md"
                echo "Converting $file -> $output_file (year=$year)"
                java -cp saxon.jar:xml-resolver.jar net.sf.saxon.Transform \
                  -s:"$file" \
                  -xsl:transform.xsl \
                  -o:"$output_file"
                if [ $? -ne 0 ]; then
                  echo "Error converting $file"
                  exit 1
                fi
              fi
            fi
          done

      - name: Commit and push changes
        run: |
          cd CavrianaCorr_FrontEnd
          git config --local user.email "github-actions[bot]@users.noreply.github.com"
          git config --local user.name "github-actions[bot]"
          git add docs/
          git diff --cached --quiet || git commit -m "Update converted Markdown files"
          git push origin main
