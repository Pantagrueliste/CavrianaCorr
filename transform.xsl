<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="tei xs"
    version="2.0">

  <!-- Produce text output (not HTML), but we will embed raw HTML tags
       by escaping them and using disable-output-escaping. -->
  <xsl:output method="text" encoding="UTF-8"/>
  <xsl:strip-space elements="tei:*"/>

  <!-- 1)  Entry point: collect entire text, then strip spaces before punctuation. -->
  <xsl:template match="/">
    <xsl:variable name="rawOutput">
      <xsl:apply-templates select="tei:TEI"/>
    </xsl:variable>
    <xsl:value-of select="replace($rawOutput, '[ \t\r\n]+([,;:\.])', '$1')"/>
  </xsl:template>

  <!-- 2) Process root <TEI> to output front matter, then apply templates to the text. -->
  <xsl:template match="tei:TEI">
    <xsl:variable name="locusFrom" select="tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msContents/tei:msItem/tei:locus/@from"/>
    <xsl:variable name="locusTo"   select="tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msContents/tei:msItem/tei:locus/@to"/>

    <xsl:variable name="archiveRef" as="xs:string" 
      select="normalize-space(
        concat(
          tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msIdentifier/tei:settlement, ' ',
          tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msIdentifier/tei:repository, ', ',
          tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msIdentifier/tei:collection, ', ',
          tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msIdentifier/tei:idno,
          ', fols. ', $locusFrom, '-', $locusTo
        )
      )"/>

    <!-- YAML-like front matter for Markdown -->
    <xsl:text>---&#10;</xsl:text>

    <xsl:text>title: "</xsl:text>
    <xsl:value-of select="concat(
      tei:teiHeader/tei:profileDesc/tei:correspDesc/tei:correspAction[@type='received']/tei:persName,
      ' (',
      tei:teiHeader/tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/tei:date/@when,
      ')'
    )"/>
    <xsl:text>"&#10;</xsl:text>

    <xsl:text>expeditor: "</xsl:text>
    <xsl:value-of select="tei:teiHeader/tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/tei:persName"/>
    <xsl:text>"&#10;</xsl:text>

    <xsl:text>addressee: "</xsl:text>
    <xsl:value-of select="tei:teiHeader/tei:profileDesc/tei:correspDesc/tei:correspAction[@type='received']/tei:persName"/>
    <xsl:text>"&#10;</xsl:text>

    <xsl:text>date: "</xsl:text>
    <xsl:value-of select="tei:teiHeader/tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/tei:date/@when"/>
    <xsl:text>"&#10;</xsl:text>

    <xsl:text>placeOfOrigin: "</xsl:text>
    <xsl:value-of select="tei:teiHeader/tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/tei:placeName"/>
    <xsl:text>"&#10;</xsl:text>

    <xsl:text>archiveRef: "</xsl:text>
    <xsl:value-of select="$archiveRef"/>
    <xsl:text>"&#10;</xsl:text>

    <xsl:text>---&#10;</xsl:text>
    <xsl:text>&#10;</xsl:text>

    <!-- Now apply templates to the text body -->
    <xsl:apply-templates select="tei:text"/>
  </xsl:template>

  <!-- 3) <text> just applies recursively. -->
  <xsl:template match="tei:text">
    <xsl:apply-templates/>
  </xsl:template>

  <!-- 4) Page breaks. -->
  <xsl:template match="tei:pb">
    <xsl:text>&#10;**[fol. </xsl:text>
    <xsl:value-of select="@n"/>
    <xsl:text>]**&#10;&#10;</xsl:text>
  </xsl:template>

  <!-- 5) Line breaks, with special handling of @break='no'. -->
<xsl:template match="tei:lb">
  <span class="lb-marker"></span>
  <xsl:text> </xsl:text>
</xsl:template>

  <!-- 6) Paragraph-like elements: after them, output blank lines. -->
  <xsl:template match="tei:p | tei:opener | tei:closer | tei:postscript">
    <xsl:apply-templates/>
    <xsl:text>&#10;&#10;</xsl:text>
  </xsl:template>

  <!-- 7) Normalise persName/placeName text. -->
  <xsl:template match="tei:persName | tei:placeName">
    <xsl:value-of select="normalize-space(.)"/>
  </xsl:template>

  <!-- 8) <choice>: only show the <expan>, ignore <abbr>. -->
  <xsl:template match="tei:choice">
    <xsl:value-of select="tei:expan"/>
    <xsl:text> </xsl:text>
  </xsl:template>
  <xsl:template match="tei:choice/tei:abbr"/>

  <!-- 9) UNCLEAR words => Insert raw <span> in text with disable-output-escaping. -->
  <xsl:template match="tei:unclear">
    <!-- We must use escaped &lt; and &gt; so the XSLT parser doesn't see them as real tags.
         Then disable-output-escaping so the final .md shows <span> literally. -->
    <xsl:text disable-output-escaping="yes">&lt;span class="unclear"&gt;</xsl:text>
    <xsl:value-of select="."/>
    <xsl:text disable-output-escaping="yes">&lt;/span&gt;</xsl:text>
  </xsl:template>

  <!-- 10) Skip <del>. -->
  <xsl:template match="tei:del"/>

  <!-- 11) <add> => inline. -->
  <xsl:template match="tei:add">
    <xsl:value-of select="."/>
  </xsl:template>

  <!-- 12) Optional note handling. -->
  <xsl:template match="tei:note">
    <xsl:text>[NOTE: </xsl:text>
    <xsl:apply-templates/>
    <xsl:text>]</xsl:text>
  </xsl:template>

  <!-- 13) Gaps and damage placeholders. -->
  <xsl:template match="tei:gap">
    <xsl:text>[missing </xsl:text>
    <xsl:value-of select="@quantity"/>
    <xsl:text> </xsl:text>
    <xsl:value-of select="@unit"/>
    <xsl:text>]</xsl:text>
  </xsl:template>

  <xsl:template match="tei:damage">
    <xsl:apply-templates/>
  </xsl:template>

  <!-- 14) Segments or unhandled TEI -> apply templates. -->
  <xsl:template match="tei:seg">
    <xsl:apply-templates/>
  </xsl:template>

  <!-- 15) Catch-all for any TEI element not matched above. -->
  <xsl:template match="tei:*">
    <xsl:apply-templates/>
  </xsl:template>

</xsl:stylesheet>
