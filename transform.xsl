<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet 
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
  xmlns:tei="http://www.tei-c.org/ns/1.0"
  xmlns:xs="http://www.w3.org/2001/XMLSchema"
  exclude-result-prefixes="tei xs"
  version="2.0">

  <xsl:output method="text" encoding="UTF-8"/>
  <xsl:strip-space elements="tei:*"/>

  <!-- Root Template -->
  <xsl:template match="/">
    <xsl:variable name="rawOutput">
      <xsl:apply-templates select="tei:TEI"/>
    </xsl:variable>
  <xsl:value-of select="replace(string-join($rawOutput, ''), '\s+([,;:\.])', '$1')"/>
  </xsl:template>

  <!-- TEI Document Template -->
  <xsl:template match="tei:TEI">
    <xsl:variable name="header" select="tei:teiHeader"/>
    <xsl:variable name="locus" select="$header/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msContents/tei:msItem/tei:locus"/>
    <xsl:variable name="msId" select="$header/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msIdentifier"/>
    <xsl:variable name="correspDesc" select="$header/tei:profileDesc/tei:correspDesc"/>

    <!-- Archive Reference -->
    <xsl:variable name="archiveRef" as="xs:string">
      <xsl:value-of select="normalize-space(concat(
        $msId/tei:settlement, ' ',
        $msId/tei:repository, ', ',
        $msId/tei:collection, ', ',
        $msId/tei:idno, ', fols. ',
        $locus/@from, '-', $locus/@to
      ))"/>
    </xsl:variable>

    <!-- YAML Metadata -->
    <xsl:text>---&#10;</xsl:text>
    <xsl:text>title: "</xsl:text>
    <xsl:value-of select="concat(
      $correspDesc/tei:correspAction[@type='received']/tei:persName,
      ' (',
      $correspDesc/tei:correspAction[@type='sent']/tei:date/@when,
      ')'
    )"/>
    <xsl:text>"&#10;</xsl:text>

    <xsl:text>expeditor: "</xsl:text>
    <xsl:value-of select="$correspDesc/tei:correspAction[@type='sent']/tei:persName"/>
    <xsl:text>"&#10;</xsl:text>

    <xsl:text>addressee: "</xsl:text>
    <xsl:value-of select="$correspDesc/tei:correspAction[@type='received']/tei:persName"/>
    <xsl:text>"&#10;</xsl:text>

    <xsl:text>date: "</xsl:text>
    <xsl:value-of select="$correspDesc/tei:correspAction[@type='sent']/tei:date/@when"/>
    <xsl:text>"&#10;</xsl:text>

    <xsl:text>placeOfOrigin: "</xsl:text>
    <xsl:value-of select="$correspDesc/tei:correspAction[@type='sent']/tei:placeName"/>
    <xsl:text>"&#10;</xsl:text>

    <xsl:text>archiveRef: "</xsl:text>
    <xsl:value-of select="$archiveRef"/>
    <xsl:text>"&#10;</xsl:text>
    <xsl:text>---&#10;&#10;</xsl:text>

    <!-- Manuscript Summary Preamble -->
    <xsl:text>**Manuscript source:** </xsl:text>
    <xsl:value-of select="$archiveRef"/>
    <xsl:text>&#10;</xsl:text>

    <xsl:if test="tei:text/tei:note[@type='summary']">
      <xsl:text>**Summary:** </xsl:text>
      <xsl:value-of select="tei:text/tei:note[@type='summary']"/>
      <xsl:text>&#10;&#10;</xsl:text>
    </xsl:if>

    <xsl:apply-templates select="tei:text"/>
  </xsl:template>

  <!-- Text Body Templates -->
  <xsl:template match="tei:text | tei:opener | tei:closer | tei:p">
    <xsl:apply-templates/>
    <xsl:text>&#10;&#10;</xsl:text>
  </xsl:template>

  <xsl:template match="tei:pb">
    <xsl:text>&#10;**[fol. </xsl:text>
    <xsl:value-of select="@n"/>
    <xsl:text>]**&#10;&#10;</xsl:text>
  </xsl:template>

  <xsl:template match="tei:lb">
    <xsl:choose>
      <xsl:when test="@break='no'">
        <xsl:text>-&#10;</xsl:text>
      </xsl:when>
      <xsl:otherwise>
        <xsl:text>&#10;</xsl:text>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <!-- Inline Elements -->
  <xsl:template match="tei:persName | tei:placeName">
    <xsl:value-of select="normalize-space(.)"/>
  </xsl:template>

  <xsl:template match="tei:choice">
    <xsl:value-of select="tei:expan"/>
    <xsl:text> </xsl:text>
  </xsl:template>

  <!-- Suppressed Elements -->
  <xsl:template match="tei:abbr | tei:del"/>

  <xsl:template match="tei:unclear">
    <xsl:text disable-output-escaping="yes">&lt;span style="text-decoration: underline wavy;"&gt;</xsl:text>
    <xsl:value-of select="."/>
    <xsl:text disable-output-escaping="yes">&lt;/span&gt;</xsl:text>
  </xsl:template>

  <xsl:template match="tei:add">
    <xsl:value-of select="."/>
  </xsl:template>

</xsl:stylesheet>
