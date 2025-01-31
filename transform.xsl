<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:tei="http://www.tei-c.org/ns/1.0"
  exclude-result-prefixes="tei"
  version="2.0">

  <xsl:output method="text" encoding="UTF-8"/>

  <!-- Main Template -->
  <xsl:template match="tei:TEI">
    <!-- YAML Front Matter -->
    <xsl:text>---&#10;</xsl:text>

    <!-- Title -->
    <xsl:text>title: "</xsl:text>
    <xsl:value-of select="
      concat(
        'to ',
        tei:teiHeader/tei:profileDesc/tei:correspDesc/tei:correspAction[@type='received']/tei:persName,
        ' (',
        tei:teiHeader/tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/tei:date/@when,
        ')'
      )
    "/>
    <xsl:text>"&#10;</xsl:text>

    <!-- Expeditor -->
    <xsl:text>expeditor: "</xsl:text>
    <xsl:value-of select="tei:teiHeader/tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/tei:persName"/>
    <xsl:text>"&#10;</xsl:text>

    <!-- Addressee -->
    <xsl:text>addressee: "</xsl:text>
    <xsl:value-of select="tei:teiHeader/tei:profileDesc/tei:correspDesc/tei:correspAction[@type='received']/tei:persName"/>
    <xsl:text>"&#10;</xsl:text>

    <!-- Date (from @when) -->
    <xsl:text>date: "</xsl:text>
    <xsl:value-of select="tei:teiHeader/tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/tei:date/@when"/>
    <xsl:text>"&#10;</xsl:text>

    <!-- Place of Origin -->
    <xsl:text>placeOfOrigin: "</xsl:text>
    <xsl:value-of select="tei:teiHeader/tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/tei:placeName"/>
    <xsl:text>"&#10;</xsl:text>

    <!-- Archive Reference -->
    <xsl:text>archiveRef: "</xsl:text>
    <xsl:value-of select="
      normalize-space(
        concat(
          tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msIdentifier/tei:settlement, ' ',
          tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msIdentifier/tei:repository, ', ',
          tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msIdentifier/tei:collection, ', ',
          tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msIdentifier/tei:idno,
          ', fols. ',
          tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msContents/tei:msItem/tei:locus/@from,
          '-',
          tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msContents/tei:msItem/tei:locus/@to
        )
      )
    "/>
    <xsl:text>"&#10;</xsl:text>

    <xsl:text>---&#10;&#10;</xsl:text>

    <!-- Printed Metadata in the body -->
    <xsl:text>**Expeditor**: </xsl:text>
    <xsl:value-of select="tei:teiHeader/tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/tei:persName"/>
    <xsl:text>  &#10;</xsl:text>

    <xsl:text>**Addressee**: </xsl:text>
    <xsl:value-of select="tei:teiHeader/tei:profileDesc/tei:correspDesc/tei:correspAction[@type='received']/tei:persName"/>
    <xsl:text>  &#10;</xsl:text>

    <xsl:text>**Date**: </xsl:text>
    <xsl:value-of select="tei:teiHeader/tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/tei:date/@when"/>
    <xsl:text>  &#10;</xsl:text>

    <xsl:text>**Place of Origin**: </xsl:text>
    <xsl:value-of select="tei:teiHeader/tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/tei:placeName"/>
    <xsl:text>  &#10;</xsl:text>

    <xsl:text>**Archive Reference**: </xsl:text>
    <xsl:value-of select="
      normalize-space(
        concat(
          tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msIdentifier/tei:settlement, ' ',
          tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msIdentifier/tei:repository, ', ',
          tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msIdentifier/tei:collection, ', ',
          tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msIdentifier/tei:idno,
          ', fols. ',
          tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msContents/tei:msItem/tei:locus/@from,
          '-',
          tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msContents/tei:msItem/tei:locus/@to
        )
      )
    "/>
    <xsl:text>  &#10;&#10;</xsl:text>

    <!-- Now output the <text> body as Markdown. -->
    <xsl:apply-templates select="tei:text"/>
  </xsl:template>

  <!-- Make <pb n="288r"/> appear as a heading: **[fol. 288r]** -->
  <xsl:template match="tei:pb">
    <xsl:text>&#10;**[fol. </xsl:text>
    <xsl:value-of select="@n"/>
    <xsl:text>]**&#10;</xsl:text>
  </xsl:template>

  <!-- Turn <lb/> into a line break, unless @break="no", in which case insert a dash -->
  <xsl:template match="tei:lb">
    <xsl:choose>
      <xsl:when test="@break='no'">
        <xsl:text>-</xsl:text>
        <xsl:text>  &#10;</xsl:text>
      </xsl:when>
      <xsl:otherwise>
        <xsl:text>  &#10;</xsl:text>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <!-- Paragraphs become double-spaced lines in Markdown. -->
  <xsl:template match="tei:p">
    <xsl:apply-templates/>
    <xsl:text>&#10;&#10;</xsl:text>
  </xsl:template>

  <xsl:template match="tei:opener">
    <xsl:apply-templates/>
    <xsl:text>&#10;&#10;</xsl:text>
  </xsl:template>

  <xsl:template match="tei:closer">
    <xsl:apply-templates/>
    <xsl:text>&#10;&#10;</xsl:text>
  </xsl:template>

  <!-- Expand <choice><abbr/><expan/></choice> into the expanded text only. -->
  <xsl:template match="tei:choice">
    <xsl:value-of select="tei:expan"/>
  </xsl:template>

  <!-- Skip <abbr> content, since we prefer the expanded text. -->
  <xsl:template match="tei:choice/tei:abbr"/>

  <!-- Minimal pass-through templates for various elements. -->
  <xsl:template match="tei:persName | tei:placeName | tei:unclear | tei:add">
    <xsl:value-of select="."/>
  </xsl:template>

  <!-- Skip <del/> entirely. -->
  <xsl:template match="tei:del"/>

  <!-- No special transformation needed for <text>. Just process children. -->
  <xsl:template match="tei:text">
    <xsl:apply-templates/>
  </xsl:template>
  
</xsl:stylesheet>
