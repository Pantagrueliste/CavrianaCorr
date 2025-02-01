<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet 
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
  xmlns:tei="http://www.tei-c.org/ns/1.0"
  xmlns:xs="http://www.w3.org/2001/XMLSchema"
  exclude-result-prefixes="tei xs"
  version="2.0">

  <xsl:output method="text" encoding="UTF-8"/>
  <!-- Remove incidental whitespace -->
  <xsl:strip-space elements="tei:*"/>

  <!-- Root template: capture output, join into a single string, then post-process -->
  <xsl:template match="/">
    <!-- Capture output from processing TEI into a variable (sequence) -->
    <xsl:variable name="rawOutput">
      <xsl:apply-templates select="tei:TEI"/>
    </xsl:variable>
    <!-- Join all items into one string -->
    <xsl:variable name="rawOutputString" as="xs:string" select="string-join($rawOutput, '')"/>
    <!-- Remove extra whitespace preceding punctuation -->
    <xsl:value-of select="replace($rawOutputString, '\s+([,;:\.\-])', '$1')"/>
  </xsl:template>

  <!-- Process the TEI document -->
  <xsl:template match="tei:TEI">
    <!-- Define folio locus values (expected as attributes) -->
    <xsl:variable name="locusFrom" select="tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msContents/tei:msItem/tei:locus/@from"/>
    <xsl:variable name="locusTo"   select="tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msContents/tei:msItem/tei:locus/@to"/>
    <xsl:variable name="archiveRef" as="xs:string" select="normalize-space(
      concat(
        tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msIdentifier/tei:settlement, ' ',
        tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msIdentifier/tei:repository, ', ',
        tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msIdentifier/tei:collection, ', ',
        tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msIdentifier/tei:idno, ', fols. ',
        $locusFrom,
        '-',
        $locusTo
      )
    )"/>

    <!-- YAML front matter -->
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
    <xsl:text>]**&#10;&#10;</xsl:text>
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
  
  <!-- Inline elements: normalize text -->
  <xsl:template match="tei:persName | tei:placeName">
    <xsl:value-of select="normalize-space(.)"/>
  </xsl:template>
  
  <!-- For choice elements, output the expansion and a trailing space -->
  <xsl:template match="tei:choice">
    <xsl:value-of select="tei:expan"/>
    <xsl:text> </xsl:text>
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
