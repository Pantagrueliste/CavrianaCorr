<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet 
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
  xmlns:tei="http://www.tei-c.org/ns/1.0" 
  exclude-result-prefixes="tei" 
  version="2.0">

  <xsl:output method="text" encoding="UTF-8"/>
  <!-- Remove incidental whitespace from TEI elements -->
  <xsl:strip-space elements="tei:*"/>

  <!-- Define a variable for archive reference (DRY) -->
  <xsl:variable name="archiveRef" as="xs:string">
    <xsl:value-of select="normalize-space(
      concat(
        tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msIdentifier/tei:settlement, ' ',
        tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msIdentifier/tei:repository, ', ',
        tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msIdentifier/tei:collection, ', ',
        tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msIdentifier/tei:idno, ', fols. ',
        tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msContents/tei:msItem/tei:locus/@from,
        '-',
        tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msContents/tei:msItem/tei:locus/@to
      )
    )"/>
  </xsl:variable>

  <xsl:template match="tei:TEI">
    <!-- YAML Front Matter -->
    <xsl:text>---&#10;</xsl:text>
    <xsl:text>title: "</xsl:text>
    <xsl:value-of select="
      concat(
        tei:teiHeader/tei:profileDesc/tei:correspDesc/tei:correspAction[@type='received']/tei:persName,
        ' (',
        tei:teiHeader/tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/tei:date/@when,
        ')'
      )
    "/>
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
    <xsl:text>---&#10;&#10;</xsl:text>

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
    <xsl:value-of select="$archiveRef"/>
    <xsl:text>  &#10;&#10;</xsl:text>

    <xsl:apply-templates select="tei:text"/>
  </xsl:template>

  <xsl:template match="tei:text">
    <xsl:apply-templates/>
  </xsl:template>

  <xsl:template match="tei:pb">
    <xsl:text>&#10;**[fol. </xsl:text>
    <xsl:value-of select="@n"/>
    <xsl:text>]**&#10;</xsl:text>
  </xsl:template>

  <xsl:template match="tei:lb">
    <xsl:choose>
      <xsl:when test="@break='no'">
        <xsl:text>-  &#10;</xsl:text>
      </xsl:when>
      <xsl:otherwise>
        <xsl:text>  &#10;</xsl:text>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

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

  <!-- Normalize text content in inline elements -->
  <xsl:template match="tei:persName | tei:placeName">
    <xsl:value-of select="normalize-space(.)"/>
  </xsl:template>

  <xsl:template match="tei:choice">
    <xsl:value-of select="tei:expan"/>
  </xsl:template>

  <xsl:template match="tei:choice/tei:abbr"/>
  <xsl:template match="tei:del"/>
  <xsl:template match="tei:unclear">
    <xsl:value-of select="."/>
  </xsl:template>
  <xsl:template match="tei:add">
    <xsl:value-of select="."/>
  </xsl:template>

</xsl:stylesheet>